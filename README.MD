1- Program Python 3.8.10'da test edilmiştir. Diğer sürümlerde hatalarla karşılaşılabilir.

2- VirtualAssistant klasörünü Visual Studio Code'da açmanız önerilir. Testler Visual Studio Code IDE'sinde yapılmıştır. Diğer IDE'lerde dosya yolu hatalarıyla karşılaşılabilir.

3- Klasörün içinde Virtual Environment oluşturmanız önerilir. Böylece bilgisayarınızdaki diğer paketlerin kurulumunu ve sürümünü etkilemez.

4- Virtual environment oluşturmak için Visual Studio Code içinde terminal açıp 
"python -m venv {isim}"
komutunu girerek kurulumun tamamlanmasını bekleyiniz.

5- Oluşturulan Virtual Environment'i etkinleştirmek için terminale 
"{isim}/Scripts/activate"
komutunu giriniz.

6- Virtual Environment aktifleştirildikten sonra 
"python --version"
ile python versiyonunu kontrol edebilirsiniz.

7- Ardından paket bağımlılıklarını kurmak için terminale 
"pip install -r requirements.txt" 
komutunu giriniz. Kurulumun tamamlanmasını bekleyiniz. Eğer kurulum sırasında hata alırsanız aşağıda kütüphanelerin versiyonsuz isimleri yazmaktadır. Orayı kopyalayıp requirements.txt dosyasına yapıştırın, dosyayı kaydedin. Ardından yukarıdaki komutu tekrar çalıştırın.

8- Kurulumlar tamamlandıktan sonra 
"pip list" 
komutuyla Virtual Environment'te yüklü olan paketleri görüntüleyebilirsiniz.

9- Kodu çalıştırmadan önce internet bağlantınızın olduğundan emin olun. Kodu çalıştırmak için Virtual Environment aktifken terminale 
"python ./Codes/main.py" 
komutunu yazınız. Kodun ilk başta çalışması uzun sürebilir bekleyiniz.

10 - Herhangi bir hata durumunda 
"python ./reset_data.py" 
komutuyla verileri sıfırlayabilirsiniz.


ÖNEMLİ NOT
----------
* Ses tanıma işlemleri için google-cloud-speech kütüphanesinin API'si kullanılmıştır. Sınırlı ücretsiz kullanım sunulmaktadır. Kullanım kotası dolduğunda hata verebilir. Eğer hatayla karşılaşırsanız https://cloud.google.com/ adresinden giriş yaparak sınırlı ücretsiz kullanıma sahip olabilirsiniz. Ardından yeni bir proje anahtarı (key) oluşturmanız gerekmektedir. Anahtarla ilgili bilgileri belirtilen adresten json formatında indirerek dosya ismini "google-api.json" olarak değiştirip proje dizinine atarak programı çalıştırabilirsiniz. 


*************************************************************************************************************************************************
Eğer requirements.txt çalışmazsa aşağıda *lar arasındaki kısmı kopyalayıp requirements.txt dosyasına yapıştırıp kaydedin.
*************************************************************************************************************************************************
bs4
google-cloud-speech
gtts
mutagen
numpy
opencv-contrib-python
openpyxl
pillow
PyAudio
pyautogui
pygame
pywhatkit
requests
SpeechRecognition
wikipedia

*************************************************************************************************************************************************

Aşağıda kodun test edildiği anda Virtual Environment'te yüklü olan modüller ve sürümleri belirtilmiştir.   


Package                  Version
------------------------ --------
beautifulsoup4           4.12.3
blinker                  1.8.2
bs4                      0.0.2
cachetools               5.3.3
certifi                  2024.2.2
charset-normalizer       3.3.2
click                    8.1.7
colorama                 0.4.6
et-xmlfile               1.1.0
flask                    3.0.3
google-api-core          2.19.0
google-auth              2.29.0
google-cloud-speech      2.26.0
googleapis-common-protos 1.63.0
grpcio                   1.63.0
grpcio-status            1.62.2
gTTS                     2.5.1
idna                     3.7
importlib-metadata       7.1.0
itsdangerous             2.2.0
jinja2                   3.1.4
MarkupSafe               2.1.5
MouseInfo                0.1.3
mutagen                  1.47.0
numpy                    1.24.4
opencv-contrib-python    4.9.0.80
openpyxl                 3.1.2
pillow                   10.3.0
pip                      21.1.1
proto-plus               1.23.0
protobuf                 4.25.3
pyasn1                   0.6.0
pyasn1-modules           0.4.0
PyAudio                  0.2.14
PyAutoGUI                0.9.54
pygame                   2.5.2
PyGetWindow              0.0.9
PyMsgBox                 1.0.9
pyperclip                1.8.2
PyRect                   0.2.0
PyScreeze                0.1.30
pytweening               1.2.0
pywhatkit                5.4
requests                 2.31.0
rsa                      4.9
setuptools               56.0.0
soupsieve                2.5
SpeechRecognition        3.10.4
typing-extensions        4.11.0
urllib3                  2.2.1
werkzeug                 3.0.3
wikipedia                1.4.0
zipp                     3.18.2


