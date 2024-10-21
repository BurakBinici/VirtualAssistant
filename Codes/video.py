import cv2
import numpy as np
import os, time
from PIL import Image
from common import *
import csv
from values import target


TRAINER_PATH = "./trainer/trainer.yaml"
JSON_PATH = "./config.json"
LOG_PATH = "./Texts/Log/"
GREET_PATH = f"{LOG_PATH}/last_greet.txt"
MEET_PATH = f"{LOG_PATH}/last_meet.txt"
LAST_SPOKEN_PATH = F"{LOG_PATH}/last_spoken_data.txt"
NAMES_PATH = f"{LOG_PATH}/names.txt"

FACE_CASCADE = cv2.CascadeClassifier("./xml/haarcascade_frontalface_default.xml")
FONT = cv2.FONT_HERSHEY_SIMPLEX
WIDTH, HEIGHT = (640, 480)
FRAME_CENTER = (WIDTH//2, HEIGHT//2)

ASSISTANT_NAME = str(read_json_file(JSON_PATH)["ASSISTANT_NAME"])

distance_dict = {}
center_dict = {}
spoken_dict = {}
prev_ft = 0
FACE_RECOG_DATA = [-1, "", (-1, -1)]


def face_recog_data(id: int, name: str, center_loc: tuple):
    return [id, name, center_loc]


def read_names_txt():
    try:
        data_dict = {}
        with open(NAMES_PATH, 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    id, name = row
                    id = int(id)
                    data_dict[id] = name
        return data_dict
    except FileNotFoundError:
        print(f"Hata: '{NAMES_PATH} adresindeki dosya bulunamadı!")
    except Exception as e:
        print(f"Hata: {e}")


def input_image_and_train(face_id: int, name: str, recognizer: cv2.face.LBPHFaceRecognizer, max_count: int=400):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    count = 0
    face_id += 1
    while cap.isOpened():
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            center = int((x + x + w) / 2), int((y + y + h) / 2)
            # cv2.putText(frame, f"{center}", center, FONT, 0.8, (0, 255, 0))
            roi_gray = gray[y:y + h, x:x + w]

            cv2.imwrite(f"./dataset/User." + str(face_id) + '.' + str(count).zfill(4) + ".jpg", roi_gray)
            count += 1
        cv2.imshow('image', frame)
        KEY = cv2.waitKey(30) & 0xff
        if KEY == 27:
            break    
        elif count >= max_count:
            break

    print("\nYüz tanıması tamamlandı.")
    cap.release()
    cv2.destroyAllWindows()

    train(recognizer, name)
    data = "{0},{1}\n".format(face_id, name)
    write_text_file(NAMES_PATH, data)
    write_json_file(JSON_PATH, "LAST_ID", face_id)


def get_images_and_labels(DATASET_PATH: str="./dataset/"):
    image_paths = [os.path.join(DATASET_PATH, f) for f in os.listdir(DATASET_PATH)]
    face_samples = []
    ids = []

    for imagePath in image_paths:
        pil_img = Image.open(imagePath).convert('L')
        img_numpy = np.array(pil_img, 'uint8')

        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = FACE_CASCADE.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y + h, x:x + w])
            ids.append(id)

    return face_samples, ids


def train(recognizer: cv2.face.LBPHFaceRecognizer, name: str):
    print("\n[BİLGİ] Eğitim işlemi başlıyor. Lütfen birkaç saniye bekleyin...")
    
    faces, ids = get_images_and_labels()
    recognizer.train(faces, np.array(ids))
    recognizer.write(TRAINER_PATH)
    # recognizer.read(TRAINER_PATH)  # recognizer.save() worked on Mac, but not on Pi

    print("\n[BİLGİ] {0} kişisinin yüzü tanımlandı. \nSisteme kayıtlı kişi sayısı: {1} \nProgramdan çıkış yapılıyor...".format(name, len(np.unique(ids))))


def recognize(shared_flag, is_running):
    GREET_TIME_THRESHOLD = 20 * 60
    MEET_TIME_THRESHOLD = 5 * 60
    STEP = 30

    last_recogn_id = -1
    is_spoken = False
    distance = 9999
    
    recognizer = cv2.face.LBPHFaceRecognizer.create()
    prev_ft = 0
    knownflag = 0
    names = {}
            
    is_empty = True if read_text_file(TRAINER_PATH) == "" else False

    if is_empty:
        try_meet(recognizer, shared_flag, is_running)
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

        recognizer.read(TRAINER_PATH)
        while is_running[0] == 1:
            ret, frame = cap.read()

            if not ret:
                print("Video durduruldu.")
                is_running[0] = 0
                break

            names = read_names_txt()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(cap.get(3)*0.1), int(cap.get(4)*0.1)))

            if len(faces) == 0:
                knownflag += 1
                if knownflag > 30:
                    target[0] = 0
                    target[1] = 0
                    knownflag = 0

            else:
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    id, tolerance = recognizer.predict(gray[y:y+h, x:x+w])

                    if id != last_recogn_id:
                        distance_dict[id] = distance
                        spoken_dict[id] = is_spoken

                    center = int((x+x+w)/2), int((y+y+h)/2)
                    # cv2.putText(frame, str(names[str(id)]), (x+40, y-100), FONT, 1, (255, 255, 255), 2)

                    if tolerance < 48:
                        # SIMILAR FACE
                        distance = ((FRAME_CENTER[0]-center[0])**2 + (FRAME_CENTER[1]-center[1])**2)**0.5

                        distance_dict[id] = int(distance)  
                        center_dict[id] = center   

                        names = read_names_txt()
                        nearest_face_id = min(distance_dict, key=distance_dict.get)
                        nearest_face_center = center_dict[nearest_face_id]

                        if abs(nearest_face_center[0]-FRAME_CENTER[0]) > 15 or abs(nearest_face_center[1]-FRAME_CENTER[1]) > 15:    
                            if len(faces) > 0:
                                target[0] = -((nearest_face_center[0]-FRAME_CENTER[0])/STEP)
                                target[1] = -((nearest_face_center[1]-FRAME_CENTER[1])/STEP)

                        name_title = names[id]
                        speak_name = names[nearest_face_id]
                        
                        if id != last_recogn_id and spoken_dict[id] == False:
                            current_time = int(time.time())
                            greet_text = read_text_file(GREET_PATH)
                            if greet_text == "":
                                greet(speak_name, shared_flag, is_running)
                                break
                            else:
                                greet_name, greet_time = greet_text.split(',')
                                last_greet_time = int(greet_time)

                                if speak_name != greet_name:
                                    greet(speak_name, shared_flag, is_running)
                                    break
                                else:
                                    if speak_name == greet_name and current_time - last_greet_time > GREET_TIME_THRESHOLD:
                                        greet(speak_name, shared_flag, is_running)
                                        break
                            
                            LAST_SPOKED_DATA = face_recog_data(id, speak_name, center)
                            last_recogn_id = id
                            spoken_dict[id] = True
                            write_text_file(LAST_SPOKEN_PATH, LAST_SPOKED_DATA)
                        
                        confidence = "  {0}%".format(round(100 - tolerance))

                    else:
                        # UNKNOWN FACE
                        name_title = "unknown"
                        # functionz(recognizer, shared_flag, is_running)
                        #############
                        is_spoken = spoken_dict[id]
                        #############
                        if not is_spoken:
                            current_time = int(time.time())
                            meet_text = read_text_file(MEET_PATH)
                            
                            last_meet_time = int(meet_text) if meet_text != "" else int(time.time())    # ; functionz(recognizer, shared_flag, is_running)
                            
                            if current_time - last_meet_time > MEET_TIME_THRESHOLD:
                                try_meet(recognizer, shared_flag, is_running)
                                break

                        confidence = "  {0}%".format(round(100 - tolerance))
                    
                    editted_title = edit_title(name_title)
                    
                    cv2.putText(frame, str(editted_title), (x + 5, y - 5), FONT, 1, (255, 255, 255), 2)
                    cv2.putText(frame, str(confidence), (x + 5, y + h - 5), FONT, 1, (255, 255, 0), 1)            
            new_ft = time.time()
            fps = 1 / (new_ft - prev_ft)
            prev_ft = new_ft
            cv2.putText(frame, f"{fps:.1f}", (10, 30), FONT, 1.3, (0, 0, 255), 2)  
            cv2.imshow("Camera", frame)
                        

            KEY = cv2.waitKey(1) & 0xFF
            if KEY == 27:
                is_running[0] = 0
                break
        
        cap.release()
        cv2.destroyAllWindows()


def meet(recognizer: cv2.face.LBPHFaceRecognizer, shared_flag):
    from audio import get_name, speak
    shared_flag[2] = 1
    name = get_name()
    LAST_ID = read_json_file(JSON_PATH)["LAST_ID"]
    speak("Birazdan yeni pencerede kamera açılacaktır. Lütfen kameraya bakarken yüzünüzü çeşitli yönlerde çevirerek sizi tanımama yardımcı olunuz.")
    input_image_and_train(LAST_ID, name, recognizer)
    shared_flag[2] = 0


def greet(speak_name: str, shared_flag, is_running, assistant_name: str=ASSISTANT_NAME):
    from audio import speak
    shared_flag[1] = 1
    speak(f"Merhaba {speak_name}, ben {assistant_name}. Size nasıl yardımcı olabilirim?")
    shared_flag[1] = 0
    last_greet_time = int(time.time())
    data = f"{speak_name}, {last_greet_time}"
    write_text_file(GREET_PATH, data)
    recognize(shared_flag, is_running)


def try_meet(recognizer: cv2.face.LBPHFaceRecognizer, shared_flag, is_running):
    from audio import meet_request
    shared_flag[0] = 1
    response = meet_request()
    if response:
        meet(recognizer, shared_flag)
    shared_flag[0] = 0
    last_meet_time = int(time.time())
    write_text_file(MEET_PATH, last_meet_time)
    recognize(shared_flag, is_running)


def edit_title(name_title):
    editted_title = ""
    for harf in name_title:
        if harf == "ç":
            harf = "c"
        elif harf == "ğ":
            harf = "g"
        elif harf == "ı":
            harf = "i"
        elif harf == "ö":
            harf = "o"
        elif harf == "ş":
            harf = "s"
        elif harf == "ü":
            harf = "u" 
        editted_title += harf
    return editted_title

