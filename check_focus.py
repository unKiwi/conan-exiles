import time
import pygetwindow as gw
from config import config
import global_variables

def check_focus_loop():
    previous_focus = None
    while global_variables.thread_flag == False:
        is_focus = config['conan_exiles_window_name'] not in gw.getActiveWindowTitle()
        
        if is_focus != previous_focus:
            previous_focus = is_focus
            try:
                global_variables.overlay_window.update()
            except:
                a = 1
        
        time.sleep(0.1)