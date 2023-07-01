import pyautogui
import pygame
import socketio
from src.config import config
from src.connection import sio
import time

import repository

pygame.mixer.init()
avalable_sound = pygame.mixer.Sound(config["shield_state"]['available_sound_path'])
used_sound = pygame.mixer.Sound(config["shield_state"]['used_sound_path'])

def shield_state_loop():
    while repository.thread_flag == False:
        pyautogui.sleep(1)

        if repository.shield_cool_down > 0:
            is_dead = pyautogui.locateOnScreen(config["shield_state"]['image_dead_path'], confidence=0.9)
            if is_dead is not None:
                repository.shield_cool_down = -1
                repository.overlay_window.update()
                
                try:
                    sio.emit('send_data', {
                        'dead': int(time.time() * 1000)
                    })
                except socketio.exceptions.BadNamespaceError:
                    pass

                pyautogui.sleep(6)
                continue

            repository.shield_cool_down = repository.shield_cool_down - 1
            repository.overlay_window.update()
            continue

        if repository.shield_cool_down == 0:
            avalable_sound.play()
            repository.shield_cool_down = -1

        is_shielded = pyautogui.locateOnScreen(config["shield_state"]['image_shield_path'], confidence=0.8)
        if is_shielded is not None:
            repository.shield_cool_down = config["shield_state"]['shield_cool_down']
            repository.overlay_window.update()
            used_sound.play()

            try:
                sio.emit('send_data', {
                    'shieldUsed': int(time.time() * 1000)
                })
            except socketio.exceptions.BadNamespaceError:
                pass

