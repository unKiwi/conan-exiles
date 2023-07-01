import numpy as np
import pyautogui
import socketio
from src.config import config
import repository
from src.connection import sio
import pytesseract

PYTESSERACT_CONFIG = '--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789/'
pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]

def calculer_distance(pixel, couleur_reference):
    return np.sqrt(np.sum((pixel - couleur_reference) ** 2))

def calculer_pourcentage_couleurs(region, color):
    image = pyautogui.screenshot(region=region)
    image_np = np.array(image)
    total_pixels = image_np.shape[0] * image_np.shape[1]
    
    pixels_rouges = 0
    pixels_noirs = 0
    pixels_blancs = 0
    
    for row in image_np:
        for pixel in row:
            distance_rouge = calculer_distance(pixel, color)
            distance_noir = calculer_distance(pixel, [0, 0, 0])
            distance_blanc = calculer_distance(pixel, [255, 255, 255])
            
            if distance_blanc < distance_rouge and distance_blanc < distance_noir:
                pixels_blancs += 1
            elif distance_rouge < distance_noir:
                pixels_rouges += 1
            else:
                pixels_noirs += 1
    
    pourcentage_rouge = (pixels_rouges / (total_pixels - pixels_blancs)) * 100

    bar_text_value = pytesseract.image_to_string(image, config=PYTESSERACT_CONFIG)
    if len(bar_text_value) == 0:
        return None
    
    return round(pourcentage_rouge)

def health_and_stamina_loop():
    x1 = config["bars"]["x"]
    health_y = config["bars"]["health_y"]
    stamina_y = config["bars"]["stamina_y"]
    x2 = config["bars"]["width"]
    bars_height = config["bars"]["height"]

    health_region = (x1, health_y, x2, bars_height)
    stamina_region = (x1, stamina_y, x2, bars_height)
    health_color = [90, 18, 8]
    stamina_color = [123, 89, 34]

    while repository.thread_flag == False:
        pyautogui.sleep(0.3)

        x1 = config["bars"]["x"]
        health_y = config["bars"]["health_y"]
        stamina_y = config["bars"]["stamina_y"]
        x2 = config["bars"]["width"]
        bars_height = config["bars"]["height"]

        health_region = (x1, health_y, x2, bars_height)
        stamina_region = (x1, stamina_y, x2, bars_height)
        health_color = [90, 18, 8]
        stamina_color = [184, 139, 57]


        health_value = None
        stamina_value = None
        try:
            health_value = calculer_pourcentage_couleurs(health_region, health_color)
            stamina_value = calculer_pourcentage_couleurs(stamina_region, stamina_color)
        except:
            continue

        if health_value is not None and repository.health != health_value:
            repository.health = health_value
            try:
                sio.emit('send_data', {
                    'health': health_value
                })
            except socketio.exceptions.BadNamespaceError:
                pass

        if stamina_value is not None and repository.stamina != stamina_value:
            repository.stamina = stamina_value
            try:
                sio.emit('send_data', {
                    'stamina': stamina_value
                })
            except socketio.exceptions.BadNamespaceError:
                pass