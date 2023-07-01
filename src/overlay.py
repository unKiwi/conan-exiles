import pyautogui
from src.config import config
import repository
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

    def paintEvent(self, event):
        if repository.conan_is_focus == False:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(QFont("Arial", config["shield_state"]['font_size']))

        # shield
        x = config["shield_state"]['text_x']
        y = config["shield_state"]['text_y']

        if repository.shield_cool_down <= 0:
            painter.setPen(QColor(config["shield_state"]['ready_color']))
            painter.drawText(x, y, config["shield_state"]['ready_text'])
        else:
            painter.setPen(QColor(config["shield_state"]['cool_down_color']))
            painter.drawText(x, y, str(repository.shield_cool_down))

        # chat
        x = config["translate_chat"]['text_x']
        y = config["translate_chat"]['text_y']
        painter.setFont(QFont("Arial", config["translate_chat"]['font_size']))
        painter.setPen(QColor(config["translate_chat"]['text_color']))
        rect = QRect(x, y, pyautogui.size().width, pyautogui.size().height)
        align_flags = Qt.AlignLeft | Qt.TextWordWrap

        painter.drawText(rect, align_flags, repository.translated_chat)

        # on off indicators

        # Définir la police et la taille du texte
        font = QFont('Arial', 14)
        painter.setFont(font)

        # Définir la couleur du texte
        painter.setPen(QColor('white'))

        # Définir les coordonnées x et y du texte en haut à droite
        text = "Raid detector " + ("ON" if repository.raid_detector_on else 'OFF') + "\nAuto bomb " + ("ON" if repository.auto_bomb_on else 'OFF') + "\nQueue cuter " + ("ON" if repository.queue_cuter_on else 'OFF') + "\nAuto bow " + ("ON" if repository.auto_bow_on else 'OFF')

        # Dessiner le texte à la position spécifiée
        marge = 8
        painter.drawText(QRect(0, marge, pyautogui.size().width - marge, pyautogui.size().height), Qt.AlignTop | Qt.AlignRight, text)

        # players info
        text = ""
        for player in repository.players:
            text += player.name + " " + str(player.health) + "%" + "\n"

        marge = 8
        painter.drawText(QRect(0, 0, pyautogui.size().width - marge, pyautogui.size().height - marge), Qt.AlignBottom | Qt.AlignRight, text)
