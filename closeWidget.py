from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog


class close_pianino(QMessageBox):

    def __init__(self):
        super().__init__()
        close = self.question(self, "Выход", "Хотите сохранить мелодию?",
                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            self.saving_to_a_file()

    def saving_to_a_file(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать файл', '',
            'файл (*.midi);; файл (*.wav)')[0]
        print(fname)

