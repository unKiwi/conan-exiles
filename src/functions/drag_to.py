import pyautogui
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController

mouse = Controller()
keyboard = KeyboardController()

def drag_to(x, y):
    mouse.press(Button.left)
    mouse_pos = pyautogui.position()
    mouse.move(x - mouse_pos.x, y - mouse_pos.y)
    pyautogui.sleep(0.1)
    mouse.release(Button.left)