from PyQt5.QtWidgets import QWidget, QPushButton, QGroupBox, QTextEdit
from PyQt5 import QtGui
from midi2audio import FluidSynth
from music21 import *


# класс "пианино"
class Piano(QWidget):
    Box: QGroupBox

    def __init__(self, width, height):
        super().__init__()
        self.Width = width
        self.Height = height
        self.all_link_buttons = {}
        self.all_buttons = {}
        self.flag = False
        self.name_last_button = None # текст на последней нажатой кнопке
        self.all_name_buttons = [' ' for _ in range(88)] # массив для имён кнопок
        self.press_event = {None: None}
        self.save_melody = stream.Stream() # хранит в себе ноты, тобеж мелодию
        self.text_error = ['ERROR! Вы не ввели имя файла для соxранения!', '', 'Введите имя файла для сохранения',
                           'ERROR! Вы пытаетесь сохранить пустую мелодию!']
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, self.Width, self.Height)
        self.setWindowTitle('Пианино')
        # списки нужны для нормального расположения клавиш
        spisok_black_button = [1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40, 42, 45, 47, 49, 52,
                               54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85]
        spisok_wite_button = [0, 2, 3, 5, 7, 8, 10, 12, 14, 15, 17, 19, 20, 22, 24, 26, 27, 29, 31, 32, 34, 36, 38, 39,
                              41, 43, 44, 46, 48, 50, 51, 53, 55, 56, 58, 60, 62, 63, 65, 67, 68, 70, 72, 74, 75, 77,
                              79, 80, 82, 84, 86, 87]

        # формирование белых клавиш
        for name in spisok_wite_button:
            button = QPushButton(self)
            i = spisok_wite_button.index(name)
            button.setObjectName(f'{name}')
            button.setStyleSheet('QPushButton{color: rgb(255, 100, 50);}')
            button.setGeometry(20 + i * 35, 5, 35, 81)
            button.clicked.connect(self.run)
            self.all_link_buttons[name] = button
            self.all_buttons[name] = midi.realtime.StreamPlayer(stream.Stream(note.Note(name)))

        # формирование чёрных клавиш
        for i in spisok_black_button:
            button = QPushButton(self)
            button.setObjectName(f'{i}')
            button.setStyleSheet('QPushButton{background-color:rgb(0,0,0); color: red;}')
            button.setGeometry(42 + (i - spisok_black_button.index(i) - 1) * 35, 5, 23, 61)
            button.clicked.connect(self.run)
            self.all_link_buttons[i] = button
            self.all_buttons[i] = midi.realtime.StreamPlayer(stream.Stream(note.Note(i)))

        # кнопка для настроек клавиш пианино на кнопки клавиатуры
        self.rename = QPushButton('забиндить клавиши пианино', self)
        self.rename.resize(self.rename.sizeHint())
        self.rename.setStyleSheet('QPushButton{background-color:rgb(250,30,50); color: yellow;}')
        self.rename.move(100, 100)
        self.rename.clicked.connect(self.settings)

        # кнопка для прослушивание мелодии
        self.listen = QPushButton('slyshat', self)
        self.listen.resize(self.listen.sizeHint())
        self.listen.move(100, 150)
        self.listen.clicked.connect(self.to_listen)

        # кнопка для сохранения в файл .wav
        self.save_wav = QPushButton('сохранить мелодию в формате wav', self)
        self.save_wav.resize(self.save_wav.sizeHint())
        self.save_wav.move(100, 200)
        self.save_wav.clicked.connect(self.saving_to_waving)

        self.error = QTextEdit('Введите имя файла для сохранения', self)
        self.error.resize(300, 50)
        self.error.move(100, 250)

        # настройка клавиш при запуске
        self.binding_buttons()

    # восстанавливает настройки кнопок с предыдущего выхода из приложения
    def binding_buttons(self):
        with open('settings_buttons.txt', 'r', encoding='utf-8') as f:
            spisok = f.readline()
        for i in range(88):
            name = spisok[i]
            button = self.all_link_buttons[i]
            button.setText(name)
            if name != ' ':
                self.press_event[name] = i

    def run(self):
        but = self.sender()
        key = int(but.objectName())
        self.all_buttons[key].play(blocked=False)
        self.save_melody.append(note.Note(key))
        if self.flag:
            if self.name_last_button not in self.press_event.keys():
                but.setText(f"{self.name_last_button}")
            self.press_event[self.name_last_button] = key
            self.name_last_button = None

    # воспроизведение звука
    def to_listen(self):
        midi.realtime.StreamPlayer(self.save_melody).play()

    # функция сохранения мелодии в музыкальный файл формата .wav
    def saving_to_waving(self):
        name = self.error.toPlainText()
        if name in self.text_error:
            self.error.setStyleSheet('QTextEdit{background-color:rgb(250,30,50); color: yellow;}')
            self.error.setText('ERROR! Вы не ввели имя файла для соxранения!')
        elif len(self.save_melody) == 0:
            self.error.setStyleSheet('QTextEdit{background-color:rgb(250,30,50); color: yellow;}')
            self.error.setText('ERROR! Вы пытаетесь сохранить пустую мелодию!')
        else:
            self.error.setStyleSheet('QTextEdit{background-color:rgb(50,250,30); color: yellow;}')
            self.save_melody.write('midi', 'last_save_melody.midi')
            fs = FluidSynth()
            fs.midi_to_audio('last_save_melody.midi', name + '.wav')

    # фунция сохранения настроек кнопок при закрытии приложения
    def quit(self):
        for name, indexing in self.press_event.items():
            if name != None and indexing != None:
                self.all_name_buttons[indexing] = name
        with open('settings_buttons.txt', 'w', encoding='utf-8') as f:
            f.write(''.join(self.all_name_buttons))

    # меняет флаг, что позволяет настроить клавиши пианино на клавиатуру
    def settings(self):
        if self.flag:
            self.rename.setStyleSheet('QPushButton{background-color:rgb(250,30,50); color: yellow;}')
        else:
            self.rename.setStyleSheet('QPushButton{background-color:rgb(30,250,50); color: red;}')
        self.flag = not self.flag

    # воспроизводит звук при нажатии кнопки на клавиатуры(если настроена) или сохраняет настройку на клавишу
    def keyPressEvent(self, event: QtGui.QKeyEvent):
        name = event.text()
        if self.flag:
            self.name_last_button = name
        elif name in self.press_event.keys():
            key = self.press_event[name]
            self.all_buttons[key].play()
            self.save_melody.append(note.Note(key))

