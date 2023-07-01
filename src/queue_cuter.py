import threading
import pyautogui
import repository

loop_running = False


def loop_function():
    global loop_running

    while loop_running:
        while True:
            btn = pyautogui.locateOnScreen("assets/play_online.png")

            if btn is not None:
                pyautogui.click(pyautogui.center(btn))
                pyautogui.sleep(1)
                pyautogui.click()
                pyautogui.sleep(1)
                pyautogui.click()
                break
        
        while True:
            btn = pyautogui.locateOnScreen("assets/direct_connect.png")

            if btn is not None:
                pyautogui.click(pyautogui.center(btn))
                break
        
        btn = None
        while True:
            btn = pyautogui.locateOnScreen("assets/ok_btn.png", confidence=0.98)

            if btn is not None:
                break

        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("a")
        pyautogui.keyUp("a")
        pyautogui.keyUp("ctrl")

        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("v")
        pyautogui.keyUp("v")
        pyautogui.keyUp("ctrl")

        pyautogui.click(pyautogui.center(btn))

        btn = None
        while True:
            btn = pyautogui.locateOnScreen("assets/cancel_btn.png")

            if btn is not None:
                pyautogui.click(pyautogui.center(btn))
                pyautogui.sleep(1)
                pyautogui.click()
                break

def toggle_queue_cuter_loop():
    global loop_running

    if loop_running:
        loop_running = False
    else:
        loop_running = True
        loop_thread = threading.Thread(target=loop_function)
        loop_thread.start()

    repository.queue_cuter_on = loop_running
    repository.overlay_window.update()