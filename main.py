import sys
import os
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QStackedWidget, QGridLayout, QMainWindow, QMessageBox, QMenu
from win32api import GetSystemMetrics
import _pyinstaller_hooks_contrib

from pianino import creat_music
from interface_maining import interface
from plaaay import Piano
from not_File import in_directory_not_file
from interface_main import Ui_MainWindow


# основной класс
class Main_interface(QMainWindow, Ui_MainWindow):
    stackedWidget: QStackedWidget
    menu: QMenu
    gridLayout: QGridLayout

    def __init__(self):
        super().__init__()
        self.flag_window = False
        self.Width = GetSystemMetrics(0)
        self.Height = GetSystemMetrics(1)
        self.init_UI()

    def init_UI(self):
        #uic.loadUi("interface_main.ui", self)
        self.setupUi(self)
        self.setLayout(self.gridLayout)
        self.setWindowTitle("Начальный экран")
        self.setMinimumSize(self.Width, self.Height - 100)
        if not self.starting(): # вызываем стартовую фунцию
            return
        self.inter = interface()
        self.piano = Piano(self.Width, self.Height)
        self.music_create = creat_music(self.Width, self.Height)
        self.menu.aboutToShow.connect(self.open_about)
        self.inter.create.clicked.connect(self.creating)
        self.inter.play.clicked.connect(self.playing)
        # добавляем все окна в stackedWidget
        self.stackedWidget.addWidget(self.inter)
        self.stackedWidget.addWidget(self.music_create)
        self.stackedWidget.addWidget(self.piano)
        self.stackedWidget.setCurrentWidget(self.inter)

    def starting(self):
        # вызывается при запуске и проверяет, есть ли нужные файлы
        name = 'default_sound_font.sf2'
        value = os.getcwd() + r'\fluidsynth-2.3.0-win10-x64\bin\fluidsynth.exe'
        if os.path.isfile(value) and os.path.isfile(os.getcwd() + '\\' + name):
            os.system(f'SETX {name} {value}')
            return True
        else:
            self.error()
            return False

    def error(self):
        # вызывает окно, если не установлены нужные файлы
        self.setWindowTitle('Нет файла default_sound_font.sf2 !!')
        widget_error = in_directory_not_file(self.Width, self.Height)
        self.stackedWidget.addWidget(widget_error)
        self.stackedWidget.setCurrentWidget(widget_error)
        self.statusBar().showMessage("ЗАГРУЗИТЕ ФАЙЛЫ В ОДНУ ПАПКУ С ПРИЛОЖЕНИЕМ")
        self.statusBar().setStyleSheet("background-color: rgb(255, 0, 0)")

    def creating(self):
        # меняет окно на "синтезатор"
        self.flag_window = True
        self.stackedWidget.setCurrentWidget(self.music_create)
        self.setWindowTitle("Синтезатор пианино -2.0")

    def playing(self):
        # меняет окно на "пианино"
        self.flag_window = True
        self.stackedWidget.setCurrentWidget(self.piano)
        self.setWindowTitle("пианино -1.0")

    def open_about(self):
        # появляется окно с описанием программы
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(
            'Данная программа позволяет поиграть на пианино с возможностью насторек клавиш на клавиатуре (играть). '
            'так же можно создать мелодию как в синтезаторе (создать).'
        )

        msg_box.setWindowTitle("О программе")
        msg_box.setStandardButtons(QMessageBox.Ok)

        msg_box.exec()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.flag_window:
            self.stackedWidget.currentWidget().quit()
        close = QtWidgets.QMessageBox.question(self,
                                               "Выход",
                                               "Вы и вправду хотите выйти???",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            a0.accept()
        else:
            a0.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_interface()
    ex.show()
    sys.exit(app.exec())

