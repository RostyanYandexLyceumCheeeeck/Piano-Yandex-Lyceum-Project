from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QCheckBox, QSpinBox, QStackedWidget


class Main_interface(QWidget):
    create: QPushButton
    download: QPushButton

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        uic.loadUi("interface.ui", self)