from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton
from interface import Ui_Form


# класс интерфейса, начального окна
class interface(QWidget, Ui_Form):
    create: QPushButton
    play: QPushButton

    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        #uic.loadUi("interface.ui", self)
        self.setupUi(self)


