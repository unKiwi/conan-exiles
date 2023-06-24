import threading
import pyautogui
import keyboard
import config

from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyboardController

# processing
active_bar_slot_width = config.ACTIVE_BAR_REGION[2] / 8

nb_bomb_to_craft = 0

loop_running = False  # Variable d'état pour suivre l'état de la boucle

def place_bomb(index):
    global nb_bomb_to_craft

    pyautogui.click()
    image_location = pyautogui.locateOnScreen(config.BOMB_ACTIVE_BAR_IMAGE_PATH, region=config.ACTIVE_BAR_REGION, confidence=0.8)
    if image_location is None:
        return
    slot_index = int((image_location.left - config.ACTIVE_BAR_REGION[0]) / active_bar_slot_width)
    if index != slot_index:
        nb_bomb_to_craft = nb_bomb_to_craft + 1
        return
    # pyautogui.scroll(1)

    place_bomb(index)

def craft():
    global nb_bomb_to_craft
    
    image_location = pyautogui.locateOnScreen(config.BOMB_CRAFT_IMAGE_PATH, region=config.CRAFT_REGION, confidence=0.8)

    if image_location is None:
        return
    
    bomb_pos = pyautogui.center(image_location)
    pyautogui.click(bomb_pos)

    pyautogui.sleep(1)
    pyautogui.click(config.CRAFT_POS)
    pyautogui.sleep(1)

    nb_bomb_to_craft = nb_bomb_to_craft - 10

def reload():
    global nb_bomb_to_craft
    print(nb_bomb_to_craft)

    pyautogui.press(config.INVENTORY_KEY)
    # pyautogui.click(SEARCH_BAR_POS[0], SEARCH_BAR_POS[1])
    # pyautogui.typewrite(BOMB_NAME)

    mouse = Controller()
    keyboard = KeyboardController()

    pyautogui.sleep(0.1)

    push_count = 0
    while push_count < 8:
        inventory_bomb_image = pyautogui.locateOnScreen(config.BOMB_INVENTORY_IMAGE_PATH, region=config.INVENTORY_REGION, confidence=0.8)

        if inventory_bomb_image is None:
            toggle_bomb_loop()
            break
        
        push_count = push_count + 1
        inventory_bomb_pos = pyautogui.center(inventory_bomb_image)
        keyboard.press(Key.shift)
        mouse.position = (inventory_bomb_pos)
        mouse.click(Button.left)
        keyboard.release(Key.shift)

    if nb_bomb_to_craft >= 10:
        craft()

    pyautogui.press(config.INVENTORY_KEY)


def loop_function():
    global loop_running

    while loop_running:
        # chercher une bombe
        image_location = pyautogui.locateOnScreen(config.BOMB_ACTIVE_BAR_IMAGE_PATH, region=config.ACTIVE_BAR_REGION, confidence=0.8)

        if image_location is None:
            reload()
            continue

        slot_index = int((image_location.left - config.ACTIVE_BAR_REGION[0]) / active_bar_slot_width)
        pyautogui.press(config.ACTIVE_BAR_KEY_MAP[slot_index])
        place_bomb(slot_index)

def toggle_bomb_loop():
    global loop_running

    if loop_running:
        loop_running = False
        print("Boucle arrêtée")
    else:
        loop_running = True
        print("Boucle démarrée")
        # Créer un thread pour exécuter la boucle
        loop_thread = threading.Thread(target=loop_function)
        loop_thread.start()