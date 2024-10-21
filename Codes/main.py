import multiprocessing as mp
import sys, os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from audio import process_audio
from video import recognize
from common import reset_config_json


if __name__ == "__main__":
    # The freeze_support call is only required on Windows
    if sys.platform == "win32":
        try:
            mp.freeze_support()
            is_running = mp.Array('b', [1])
            shared_flag = mp.Array('i', [0, 0, 0])

            audio_proc = mp.Process(target=process_audio, args=(shared_flag, is_running,))
            video_proc = mp.Process(target=recognize, args=(shared_flag, is_running))

            audio_proc.start()
            video_proc.start()

            audio_proc.join()
            video_proc.join()

        except KeyboardInterrupt:
            print("Program sonlandırılıyor...")
            reset_config_json()
        except Exception as e:
            print("Bir hata ile karşılaşıldı! {0}".format(e))
            reset_config_json()

