import os, time, pygame, datetime
from gtts import gTTS
from mutagen.mp3 import MP3
from collections import deque
import speech_recognition as sr
from common import *
import pyautogui, webbrowser, requests, wikipedia, pywhatkit
from bs4 import BeautifulSoup


GOOGLE_APPLICATION_CREDENTIALS = "./google-api.json"

JSON_PATH = "./config.json"
SLOCK_FILE = "slockfile.lock"
LLOCK_FILE = "llockfile.lock"
ASSISTANT_NAME = str(read_json_file(JSON_PATH)["ASSISTANT_NAME"])

mix = pygame.mixer

EXCEL_TEXT_PATH = './Texts/Excel'
RESPONSE_TEXT_PATH = './Texts/Response'

bad_state = read_text(f'{EXCEL_TEXT_PATH}/bad_state.txt')
designer = read_text(f'{EXCEL_TEXT_PATH}/designer.txt')
good_state = read_text(f'{EXCEL_TEXT_PATH}/good_state.txt')
goodbye = read_text(f'{EXCEL_TEXT_PATH}/goodbye.txt')
greet = read_text(f'{EXCEL_TEXT_PATH}/greet.txt')
howareyou = read_text(f"{EXCEL_TEXT_PATH}/howareyou.txt")
thank = read_text(f'{EXCEL_TEXT_PATH}/thank.txt')
weather = read_text(f'{EXCEL_TEXT_PATH}/weather.txt')
positive = read_text(f'{EXCEL_TEXT_PATH}/positive.txt')
negative = read_text(f'{EXCEL_TEXT_PATH}/negative.txt')

bad_response = read_text(f'{RESPONSE_TEXT_PATH}/bad_response.txt')
good_response = read_text(f'{RESPONSE_TEXT_PATH}/good_response.txt')
greet_response = read_text(f"{RESPONSE_TEXT_PATH}/greet_response.txt")
howareyou_response = read_text(f'{RESPONSE_TEXT_PATH}/howareyou_response.txt')
thank_response = read_text(f'{RESPONSE_TEXT_PATH}/thank_response.txt')

thank_response2 = read_text(f'{RESPONSE_TEXT_PATH}/thank.txt')
 

def play_audio_with_pygame(file_path):
    try:
        mix.init()
        mix.music.load(file_path)
        mix.music.play()
        while mix.music.get_busy():
            pygame.time.Clock().tick(10)
        mix.stop()
    except Exception as e:
        print(f"Error playing audio: {e}")


def write_last_msgs_txt(text, file_path: str="./Texts/Log/last_messages.txt"):
    last_messages = deque(["msg1,10", "msg2,10", "msg3,10"])
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    
    last_speak_minute = hour*60 + minute
    last_time = (hour, minute)
    element = text + "," + str(last_speak_minute)
    last_messages.append(element)
    last_messages.popleft()

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(f"{last_speak_minute}\n")
        file.write(f"{last_time}\n")
        file.write(f"{last_messages}\n")
    

def speak(text: str, lang='tr'):
    try:
        while os.path.exists(SLOCK_FILE):
            time.sleep(0.15)
        else:
            with open(SLOCK_FILE, 'w') as file:
                file.write("Locked")

            try:
                tts = gTTS(text=text, lang=lang)

                date_string = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                filename = "./sounds/voice"+date_string+".mp3"

                tts.save(filename)
                audio = MP3(filename)
                play_audio_with_pygame(filename)
                write_last_msgs_txt(text)
                os.remove(SLOCK_FILE)
            except Exception as e:
                print(f"Speaking Error: {e}")
    except KeyboardInterrupt:
        if os.path.exists(SLOCK_FILE):
            os.remove(SLOCK_FILE)


def listen(lang='tr-TR'):
    try:
        while os.path.exists(LLOCK_FILE) or os.path.exists(SLOCK_FILE):
            time.sleep(0.15)    # 0.15    
        else:
            with open(LLOCK_FILE, 'w') as file:
                file.write("Locked")
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            print("Dinleniyor...")
            recognizer.pause_threshold = 1
            recognizer.energy_threshold = 300
            audio = recognizer.listen(source, 0, 3) # ,4)
        try:
            command = recognizer.recognize_google_cloud(audio, credentials_json=GOOGLE_APPLICATION_CREDENTIALS, language=lang)  # , pfilter=1)
            print("Anlaşılan komut: " + command)
            os.remove(LLOCK_FILE)
            return str(command).lower()
        except sr.UnknownValueError:
            print("Komut anlaşılamadı.")
            os.remove(LLOCK_FILE)
            return "-"
    except KeyboardInterrupt:
        return "-l"
    except Exception as e:
        print("Bir hata ile karşılaşıldı! {0}".format(e))
        return "-e"
    finally:
        if os.path.exists(LLOCK_FILE):
            os.remove(LLOCK_FILE)
        if os.path.exists(SLOCK_FILE):
            os.remove(SLOCK_FILE)


def time_response():
        now = datetime.datetime.now()
        if 5 <= int(now.hour) < 17:
            term = "iyi günler"
        elif 17 <= int(now.hour) < 21:
            term = "iyi akşamlar"
        else:
            term = "iyi geceler"
        return term


def meet_request():
    question = random_select(read_text("./Texts/Response/meet_request.txt"))
    speak(question)
    command = listen()
    while command == "-":
        speak("Anlayamadım tekrarlar mısın?")
        command = listen()
    else:
        if find_in_array(positive, command):
            return True
        else:
            response = random_select(read_text("./Texts/Response/meet_neg_response.txt"))
            speak(response)
            return False


def get_name():
    while True:
        question = random_select(read_text("./Texts/Response/ask_name.txt"))
        speak(question)
        time.sleep(0.1)
        command = listen()
        if command == "-":
            speak("Anlayamadım tekrarlar mısın?")
        else:
            name = command
            speak(f"Emin olmak için soruyorum. Adınız {name} değil mi?")
            query = listen()
            if find_in_array(positive, query):
                speak("Tamamdır devam ediyorum.")
                return name
            else:
                speak("Kusura bakmayın.")


def process_audio(shared_flag, is_running):
    time.sleep(1.5)
    while is_running[0] == 1:
        if shared_flag[0] == 1 or shared_flag[1] == 1 or shared_flag[2] == 1:
            time.sleep(0.5)
        else:
            command = listen()   
            if command != "-":              
                if find_in_array(greet, command):
                    term = random_select(greet_response)
                    speak(f"{term}. Sizin için neler yapabilirim ?")
                elif find_in_array(good_state, command):
                    speak(random_select(good_response))

                elif find_in_array(bad_state, command):
                    speak(random_select(bad_response))
                
                elif find_in_array(thank, command):
                    speak(random_select(thank_response))

                elif find_in_array(howareyou, command):
                    speak(f"İyiyim. {random_select(thank_response2)}. {random_select(howareyou_response)}")

                elif find_in_array(designer, command):
                    OWNER = read_json_file(JSON_PATH)["OWNER"]
                    speak(f"Ben {OWNER} tarafından tasarlandım.")

                elif "youtube" in command:
                    video_title = command.replace("youtube'dan", '').strip()
                    video_title = video_title.replace("aç", '').strip()
                    speak("YouTubedan araştırma yapmaya başladım.")
                    command = command.replace("youtube arama", "")
                    command = command.replace("youtube", "")
                    command = command.replace("youtubedan", "")
                    command = command.replace(ASSISTANT_NAME, "")
                    web = "https://www.youtube.com/results?search_query=" + command
                    webbrowser.open(web)
                    pywhatkit.playonyt(command)
                    speak("Yapıldı.")

                elif "duraklat" in command:
                    pyautogui.press("k")
                    speak("video durdu")

                elif "oynat" in command:
                    pyautogui.press("k")
                    speak("video oynadı")

                elif "sesi kapat" in command:
                    pyautogui.press("m")
                    speak("video susturuldu")

                elif "arttır" in command:
                    pyautogui.press("up")
                    speak("Ses artıyor")

                elif "azalt" in command:
                    speak("Ses azalıyor")

                elif "wikipedia" in command:
                    speak("Wikipedia'dan araştırmalara başladım")
                    command = command.replace("wikipedia", "")
                    command = command.replace("search wikipedia", "")
                    command = command.replace("araştır", "")
                    command = command.replace("araştırır mısın", "")
                    command = command.replace(ASSISTANT_NAME, "")
                    try:
                        results = wikipedia.summary(command, sentences=2)
                        speak("Wikipedia'ya göre sonuçları arkadaşım açıklayacak:")
                        speak(results, lang='en')
                        print(results)
                    except Exception as e:
                        speak("Bir hata oluştu")
                        print("Bir hata oluştu!", e)
                    
                elif "google" in command:
                    speak("Google'dan arama yapıyorum.")
                    import wikipedia as googleScrap
                    command = command.replace(ASSISTANT_NAME, "")
                    command = command.replace("google araştır", "")
                    command = command.replace("google", "")
                    speak("Google'da bunları buldum. Bir bakın lütfen")
                    try:
                        pywhatkit.search(command)
                        result = googleScrap.summary(command, 1)
                        speak(result)
                    except Exception:
                        speak("Konuşulacak bir şey yok")

                elif "saat" in command:
                    strTime = datetime.datetime.now().strftime("%H:%M")
                    speak(f"Saat tam olarak {strTime}")

                elif "sıcaklık" in command:
                    search = "izmir sıcaklık"
                    url = f"https://www.google.com/search?q={search}"
                    r = requests.get(url)
                    data = BeautifulSoup(r.text, "html.parser")
                    temp = data.find("div", class_="BNeawe").text
                    speak(f"Şu anda {search} {temp}")
                    print(f"Şu anda {search} {temp}")

                elif find_in_array(goodbye, command):
                    term = time_response()
                    speak(f"Hoşça kal, {term}!")
                    is_running[0] = 0
                
                else:
                    # Daha sonraki aşamada geliştirilecektir.
                    # Komutun ChatGPT'ye gönderilip gelen yanıta göre cevap vermesi planlanmaktadır.
                    print("ChatGPT")
            else:
                print("-")

