import pyautogui
import repository
from pynput import mouse
from itertools import cycle
from src.config import config

iterateur = cycle(config["auto_bow"]["slots_key_bind"])
clic_en_cours = False

# Fonction à appeler lors du clic de souris
def on_click(x, y, button, pressed):
    global clic_en_cours

    if repository.auto_bow_on == False:
        return

    if button == mouse.Button.left:
        if pressed:
            clic_en_cours = True
        else:
            if clic_en_cours:
                pyautogui.press(next(iterateur))
                clic_en_cours = False

listener = mouse.Listener(on_click=on_click)

def toggle_bow_loop():
    global listener
    
    if repository.auto_bow_on:
        repository.auto_bow_on = False
        listener.stop()
    else:
        repository.auto_bow_on = True
        listener.start()

    repository.overlay_window.update()