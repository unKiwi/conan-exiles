import time
import pygetwindow as gw
from src.config import config
import repository

def check_focus_loop():
    while repository.thread_flag == False:
        active_window_title = gw.getActiveWindowTitle()
        if active_window_title is None:
            continue

        is_focus = config['conan_exiles_window_name'] in active_window_title
        
        if is_focus != repository.conan_is_focus:
            repository.conan_is_focus = is_focus
            try:
                repository.overlay_window.update()
            except:
                a = 1
        
        time.sleep(0.1)