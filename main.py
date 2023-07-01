import getpass
import locale
import sys
import threading
import keyboard
from src.auto_bow import toggle_bow_loop
from src.check_focus import check_focus_loop
from src.config import config
from src.drop import drop
import repository
from src.connection import sio

from PyQt5.QtWidgets import QApplication

from src.auto_bomb import toggle_bomb_loop
from src.health_and_stamina import health_and_stamina_loop
from src.overlay import Overlay
from src.queue_cuter import toggle_queue_cuter_loop
from src.raid_detector import toggle_raid_detector_loop
from src.shield_state import shield_state_loop
from src.translate_chat import remove_translation, translate_chat


username = getpass.getuser()
language, encoding = locale.getlocale()


shield_state_loop_thread = threading.Thread(target=shield_state_loop)
shield_state_loop_thread.start()

player_pos_loop_thread = threading.Thread(target=health_and_stamina_loop)
player_pos_loop_thread.start()

check_focus_loop_thread = threading.Thread(target=check_focus_loop)
check_focus_loop_thread.start()

keyboard.add_hotkey(config["auto_bomb"]["key_bind"], toggle_bomb_loop)
keyboard.add_hotkey(config["translate_chat"]["translate_key_bind"], translate_chat)
keyboard.add_hotkey(config["translate_chat"]["hide_translation_key_bind"], remove_translation)
keyboard.add_hotkey(config["drop"]["key_bind"], drop)
keyboard.add_hotkey(config["raid_detector"]["key_bind"], toggle_raid_detector_loop)
keyboard.add_hotkey(config["queue_cuter"]["key_bind"], toggle_queue_cuter_loop)
keyboard.add_hotkey(config["auto_bow"]["toggle_key_bind"], toggle_bow_loop)

app = QApplication(sys.argv)
repository.overlay_window = Overlay()
repository.overlay_window.show()
repository.overlay_window.update()
app.exec_()

repository.thread_flag = True
sio.disconnect()