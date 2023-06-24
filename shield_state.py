import pyautogui
import pygame
from config import config

import global_variables

pygame.mixer.init()
avalable_sound = pygame.mixer.Sound(config["shield_state"]['available_sound_path'])
used_sound = pygame.mixer.Sound(config["shield_state"]['used_sound_path'])

def shield_state_loop():
    while global_variables.thread_flag == False:
        pyautogui.sleep(1)

        if global_variables.shield_cool_down > 0:
            is_dead = pyautogui.locateOnScreen(config["shield_state"]['image_dead_path'], confidence=0.9)
            if is_dead is not None:
                global_variables.shield_cool_down = -1
                global_variables.overlay_window.update()
                pyautogui.sleep(6)
                continue

            global_variables.shield_cool_down = global_variables.shield_cool_down - 1
            global_variables.overlay_window.update()
            continue

        if global_variables.shield_cool_down == 0:
            avalable_sound.play()
            global_variables.shield_cool_down = -1

        is_shielded = pyautogui.locateOnScreen(config["shield_state"]['image_shield_path'], confidence=0.8)
        if is_shielded is not None:
            global_variables.shield_cool_down = config["shield_state"]['shield_cool_down']
            global_variables.overlay_window.update()
            used_sound.play()

