1- The program was tested in Python 3.8.10. Other versions may encounter errors.

2- It is recommended to open the VirtualAssistant folder in Visual Studio Code. The tests were performed in the Visual Studio Code IDE. File path errors may be encountered in other IDEs.

3- It is recommended to create a Virtual Environment in the folder. This way, it does not affect the installation and version of other packages on your computer.

4- To create a virtual environment, open a terminal in Visual Studio Code and enter the command
"python -m venv {name}"
and wait for the installation to complete.

5- To activate the created Virtual Environment, enter the command
"{name}/Scripts/activate"
in the terminal.

6- After the Virtual Environment is activated, you can check the python version with
"python --version"

7- Then enter the command
"pip install -r requirements.txt"
in the terminal to install the package dependencies. Wait for the installation to complete. If you get an error during the installation, the names of the libraries without versions are written below. Copy and paste it to the requirements.txt file, save the file. Then run the above command again.

8- After the installation is complete, you can view the packages installed in the Virtual Environment with the command
"pip list"

9- Make sure you have an internet connection before running the code. To run the code, type the command
"python ./Codes/main.py"
in the terminal while the Virtual Environment is active. The code may take a long time to run at first, wait.

10 - In case of any error, you can reset the data with the command
"python ./reset_data.py"

IMPORTANT NOTE
----------
* The google-cloud-speech library API was used for voice recognition operations. Limited free use is offered. It may give an error when the usage quota is full. If you encounter an error, you can access limited free usage by logging in to https://cloud.google.com/. Then you need to create a new project key. You can download the information about the key in json format from the specified address, change the file name to "google-api.json" and put it in the project directory and run the program.

************************************************************************************************************************************************************************
If requirements.txt does not work, copy the part between the * below and paste it into the requirements.txt file and save it.
*********************************************************************************************************************************************************
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

************************************************************************************************************************************
The modules and their versions loaded in the Virtual Environment at the time the code was tested are listed below.

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


