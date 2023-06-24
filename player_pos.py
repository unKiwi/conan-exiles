from config import TESSERACT_PATH
import pytesseract
from PIL import ImageGrab

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def player_pos_loop():
    while True:
        # Définir les coordonnées du rectangle où se trouve le texte violet
        x1, y1, x2, y2 = 117, 1055, 288, 1073

        # Capturer une partie de l'écran définie par les coordonnées
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        # Utiliser Pytesseract pour effectuer la reconnaissance optique de caractères
        text = pytesseract.image_to_string(screenshot, config='--psm 6 -c tessedit_char_whitelist=-,.0123456789 ')

        # Afficher le texte extrait
        print(text)
