import json


TESSERACT_PATH = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

# overlay
FONT_SIZE = 16

# net limiter
INPUT_SPEED_LIMIT = 1
OUTPUT_SPEED_LIMIT = 20

# shield
IMAGE_SHIELD_PATH = "./shield_crop.png"
IMAGE_DEAD_PATH = "./dead_crop.png"
SOUND_PATH = './avalaible.mp3'
READY_TEXT = "Ready"
FONT_SIZE = 24
TIME_TO_WAIT = 60
READY_TEXT = "OK"

with open('config.json') as file:
    config = json.load(file)