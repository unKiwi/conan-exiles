from src.config import config
from googletrans import Translator
import pyautogui
import pytesseract
import langid
import repository

pytesseract.pytesseract.tesseract_cmd = config["tesseract_path"]
langid.set_languages(config["translate_chat"]["src_lang"])
translator = Translator(service_urls=['translate.google.com'])

DELIMITER = ']: '

def disec_message(message):
    index = message.find(DELIMITER)

    if index != -1:
        before = message[:index]
        after = message[index + len(DELIMITER):]
        return (before, after)
    else:
        return (message, '')

def translate_chat():
    image = pyautogui.screenshot(region=(config["translate_chat"]["region"]['x'], config["translate_chat"]["region"]['y'], config["translate_chat"]["region"]['width'], config["translate_chat"]["region"]['height']))

    text = pytesseract.image_to_string(image, lang='eng+rus')

    messages = text.split('\n\n')

    repository.translated_chat = ""

    for message in messages:
        name, content = disec_message(message)

        try:
            lang, score = langid.classify(content)
            translation = translator.translate(content, src=lang, dest=config["translate_chat"]['my_lang'])
            repository.translated_chat += lang + " " + name + DELIMITER + translation.text + "\n"
        except:
            a = 1

    print(repository.translated_chat)

    repository.overlay_window.update()

def remove_translation():
    repository.translated_chat = ""
    repository.overlay_window.update()