import random, json, os, time


JLOCK_FILE = "./jlockfile.lock"


def read_json_file(path: str):
    with open(path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        return json_data


def write_json_file(path: str, key: str, value):
    try:
        while os.path.exists(JLOCK_FILE):
            time.sleep(0.15)    # 0.15
            
        else:
            with open(JLOCK_FILE, 'w') as file:
                file.write("Locked")
        data = read_json_file(path)
        with open(path, 'w', encoding='utf-8') as file:
            data[key] = value
            json.dump(data, file, ensure_ascii=False)
            os.remove(JLOCK_FILE)
    except KeyboardInterrupt:
        os.remove(JLOCK_FILE)
    except Exception as e:
        print("Bir hata oluştu! {0}".format(e))
        os.remove(JLOCK_FILE)


def find_in_array(array: list, command: str):
    new_array = []
    for element in array:
        if element != "":
            if element in command:
                new_array.append(element)
    if len(new_array) > 0:
        return True
    else:
        return False


def random_select(array: list):
    index = random.randint(0, len(array) - 1)
    term = array[index]
    return term


def read_text(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
            terms = data.split('\n')
            return terms
    except Exception as e:
        print(f"Dosya okunamadı! {e}")
        return


def reset_config_json(path: str="./config.json"):
    try:
        while os.path.exists(JLOCK_FILE):
            os.remove(JLOCK_FILE)            
        else:
            data = read_json_file(path)
            with open(path, 'w', encoding='utf-8') as file:
                data["ASSISTANT_NAME"] = "Bilge"
                data["OWNER"] = "Burak Binici, Yiğit Yıldız, Berkay Bilimli ve Ramazan Özer"
                # data["LAST_ID"] = -1
                
                json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        print(f"config.json dosyası sıfırlanamadı! {e}")
        return


def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()
    except Exception:
        print("Dosya okuma hatası!")


def write_text_file(file_path, data):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{data}")
    except Exception:
        print("Dosya yazma hatası!")

