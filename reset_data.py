import glob, os, json
from Codes.common import read_json_file


def delete_files_in_folder(folder_path):
    files = glob.glob(os.path.join(folder_path, '*'))
    for file in files:
        try:
            os.remove(file)
            print(f"{file} başarıyla silindi.")
        except Exception as e:
            print(f"{file} silinirken bir hata oluştu: {e}")


def reset_log_files(folder_path: str="./Texts/Log/"):
    files = glob.glob(os.path.join(folder_path, '*'))
    for file_path in files:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("")
                print(f"{file_path} başarıyla sıfırlandı.")
        except Exception as e:
                print(f"{file_path} sıfırlanırken bir hata oluştu: {e}")


def reset_config_json(path: str="./config.json"):
    try:
        data = read_json_file(path)
        with open(path, 'w', encoding='utf-8') as file:
            data["ASSISTANT_NAME"] = "Bilge"
            data["OWNER"] = "Burak Binici, Yiğit Yıldız, Berkay Bilimli ve Ramazan Özer"
            data["LAST_ID"] = -1
            json.dump(data, file, ensure_ascii=False)
        print(f"{path} dosyası başarıyla sıfırlandı.")
    except Exception as e:
        print(f"{path} dosyası sıfırlanamadı! {e}")
        return


def reset_trainer_file(path: str="./trainer/trainer.yaml"):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write("")
            print(f"{path} başarıyla silindi.")
    except Exception as e:
            print(f"{path} silinirken bir hata oluştu: {e}")


if __name__ == '__main__':
    delete_files_in_folder("./dataset/")
    delete_files_in_folder("./sounds/")
    reset_log_files()
    reset_trainer_file()
    reset_config_json()

