import pyautogui
from config import config
from PIL import Image

import global_variables

def health_and_stamina_loop():
    maxRed = 0
    minRed = 255
    maxGreen = 0
    minGreen = 255
    maxBlue = 0
    minBlue = 255
    while global_variables.thread_flag == False:
        screenshot = pyautogui.screenshot(region=(config["bars"]["x"], config["bars"]["health_y"], config["bars"]["width"], 1))
        screenshot.save("test.png")

        # Convertir l'image en mode RVB (Red, Green, Blue)
        image = screenshot.convert("RGB")
        
        # Obtenir les dimensions de l'image
        largeur, hauteur = image.size
        
        # Initialiser le compteur de pixels rouges
        pixels_rouges = 0
        
        # Parcourir tous les pixels de l'image

        
        for x in range(largeur):
            for y in range(hauteur):
                # Obtenir la valeur du pixel (rouge, vert, bleu)
                rouge, vert, bleu = image.getpixel((x, y))
                
                # Vérifier si le pixel est rouge (vous pouvez ajuster ces seuils en fonction de vos besoins)

                

                if rouge > maxRed:
                    maxRed = rouge
                if rouge < minRed:
                    minRed = rouge
                if vert > maxGreen:
                    maxGreen = vert
                if vert < minGreen:
                    minGreen = vert
                if bleu > maxBlue:
                    maxBlue = bleu
                if bleu < minBlue:
                    minBlue = bleu

                if rouge > 60 and rouge < 120 and vert > 20 and vert < 110 and bleu > 10 and bleu < 50:
                    pixels_rouges += 1
        
        # Calculer le pourcentage de pixels rouges
        pourcentage_rouge = (pixels_rouges / (largeur * hauteur)) * 100
        
        print(pourcentage_rouge)

    print("maxRed")
    print(maxRed)
    print("minRed")
    print(minRed)
    print("maxGreen")
    print(maxGreen)
    print("minGreen")
    print(minGreen)
    print("maxBlue")
    print(maxBlue)
    print("minBlue")
    print(minBlue)

# stam condition rouge > 70 and rouge < 160 and vert > 40 and vert < 130 and bleu > 20 and bleu < 80