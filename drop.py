import pyautogui
from config import config
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController

from functions.drag_to import drag_to

mouse = Controller()
keyboard = KeyboardController()

def drop():
    saved_mouse_pos = pyautogui.position()
    drag_to(config["drop"]["x"], config["drop"]["y"])
    pyautogui.moveTo(saved_mouse_pos)