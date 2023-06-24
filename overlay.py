import pyautogui
from config import config
import global_variables
import pygetwindow as gw

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QRect

class Overlay(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__press_pos = QPoint()

        self.initUI()

    def initUI(self):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoChildEventsForParent, True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.setGeometry(0, 0, pyautogui.size().width, pyautogui.size().height)

        self.paintEvent(self)

    def paintEvent(self, event):
        # if config['conan_exiles_window_name'] not in gw.getActiveWindowTitle():
        #     return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Arial", config["shield_state"]['font_size']))

        painter.begin(self)

        # shield
        x = config["shield_state"]['text_x']
        y = config["shield_state"]['text_y']

        if global_variables.shield_cool_down <= 0:
            painter.setPen(QColor(config["shield_state"]['ready_color']))
            painter.drawText(x, y, config["shield_state"]['ready_text'])
        else:
            painter.setPen(QColor(config["shield_state"]['cool_down_color']))
            painter.drawText(x, y, str(global_variables.shield_cool_down))

        # chat
        x = config["translate_chat"]['text_x']
        y = config["translate_chat"]['text_y']
        painter.setFont(QFont("Arial", config["translate_chat"]['font_size']))
        painter.setPen(QColor(config["translate_chat"]['text_color']))
        rect = QRect(x, y, pyautogui.size().width, pyautogui.size().height)
        align_flags = Qt.AlignLeft | Qt.TextWordWrap

        painter.drawText(rect, align_flags, global_variables.translated_chat)

        painter.end()