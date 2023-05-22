from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QMainWindow, QStatusBar


# класс окна, вызываемого, если не будут скачаны 2 нужных файла
class in_directory_not_file(QMainWindow):
    def __init__(self, width, height):
        self.Width = width
        self.Height = height
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, self.Width, self.Height)
        self.pixmap = QPixmap('dead_inside.jpg')
        self.image = QLabel(self)
        self.image.resize(self.Width, self.Height)
        self.image.move(0, 0)
        self.image.setPixmap(self.pixmap)
