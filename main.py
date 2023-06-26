import json
import sys
import threading
import keyboard
from check_focus import check_focus_loop
from config import config
from drop import drop
import global_variables
import global_variables

from PyQt5.QtWidgets import QApplication

# from auto_bomb import toggle_bomb_loop
from health_and_stamina import health_and_stamina_loop
from overlay import Overlay
from player_pos import player_pos_loop
from raid_detector import toggle_raid_detector_loop
from shield_state import shield_state_loop
from translate_chat import remove_translation, translate_chat

with open('config.json') as file:
    config = json.load(file)

shield_state_loop_thread = threading.Thread(target=shield_state_loop)
shield_state_loop_thread.start()

# player_pos_loop_thread = threading.Thread(target=player_pos_loop)
# player_pos_loop_thread.start()

# player_pos_loop_thread = threading.Thread(target=health_and_stamina_loop)
# player_pos_loop_thread.start()

# check_focus_loop_thread = threading.Thread(target=check_focus_loop)
# check_focus_loop_thread.start()

# keyboard.add_hotkey(config.BOMB_SHORTCUT, toggle_bomb_loop)
keyboard.add_hotkey(config["translate_chat"]["translate_key_bind"], translate_chat)
keyboard.add_hotkey(config["translate_chat"]["hide_translation_key_bind"], remove_translation)
keyboard.add_hotkey(config["drop"]["key_bind"], drop)
keyboard.add_hotkey(config["raid_detector"]["key_bind"], toggle_raid_detector_loop)

app = QApplication(sys.argv)
global_variables.overlay_window = Overlay()
global_variables.overlay_window.show()
global_variables.overlay_window.update()
app.exec_()

global_variables.thread_flag = True