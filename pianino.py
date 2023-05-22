from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QPushButton, QCheckBox, QSpinBox, QTextEdit
from music21 import *
from midi2audio import FluidSynth
from pianinka import Ui_Piano


# класс синтезатора
class creat_music(QWidget, Ui_Piano):
    play_melody: QPushButton
    del_all: QPushButton
    cells: QPushButton
    count_cells: QSpinBox
    error: QTextEdit

    def __init__(self, width, height):
        super().__init__()
        self.Width = width
        self.Height = height
        self.cache = {}
        self.all_checks_true = []
        self.all_checks = [[] for _ in range(88)]
        self.melody = []
        self.count_but = 50
        self.initUI()

    def initUI(self):
        spisok_name_note = ["A0", 'A0-B0', 'B0',
                            'C1', 'C1-D1', 'D1', 'D1-E1', 'E1', 'F1', 'F1-G1', 'G1', 'G1-A1', 'A1', 'A1-B1', 'B1',
                            'C2', 'C2-D2', 'D2', 'D2-E2', 'E2', 'F2', 'F2-G2', 'G2', 'G2-A2', 'A2', 'A2-B2', 'B2',
                            'C3', 'C3-D3', 'D3', 'D3-E3', 'E3', 'F3', 'F3-G3', 'G3', 'G3-A3', 'A3', 'A3-B3', 'B3',
                            'C4', 'C4-D4', 'D4', 'D4-E4', 'E4', 'F4', 'F4-G4', 'G4', 'G4-A4', 'A4', 'A4-B4', 'B4',
                            'C5', 'C2-D5', 'D5', 'D5-E5', 'E5', 'F5', 'F5-G5', 'G5', 'G5-A5', 'A5', 'A5-B5', 'B5',
                            'C6', 'C6-D6', 'D6', 'D6-E6', 'E6', 'F6', 'F6-G6', 'G6', 'G6-A6', 'A6', 'A6-B6', 'B6',
                            'C7', 'C7-D7', 'D7', 'D7-E7', 'E7', 'F7', 'F7-G7', 'G7', 'G7-A7', 'A7', 'A7-B7', 'B7',
                            'C8'
                            ]
        # список нужен для нормального расположения клавиш
        spisok_black_button = [1, 4, 6, 9, 11, 13, 16, 18, 21, 23, 25, 28, 30, 33, 35, 37, 40, 42, 45, 47, 49, 52,
                               54, 57, 59, 61, 64, 66, 69, 71, 73, 76, 78, 81, 83, 85]
        #uic.loadUi("pianinka.ui", self)
        self.setupUi(self)
        self.setFixedSize(self.Width, self.Height)
        self.setWindowTitle('Piano')

        #подлючение кнопок к нужным методам
        self.play_melody.clicked.connect(self.play_a_melody)
        self.del_all.clicked.connect(self.delit_all)
        self.cells.clicked.connect(self.add_cells)

        # формирование кнопок
        for rite in range(88):
            push = QPushButton(f"{spisok_name_note[rite]}")
            if rite in spisok_black_button:
                push.setStyleSheet('QPushButton{background-color:rgb(0,0,0); color: red;}')
            else:
                push.setStyleSheet('QPushButton{color: rgb(255, 100, 50);}')
            push.setObjectName(f'{rite}')
            push.clicked.connect(self.clicked_note)
            self.gridLayout.addWidget(push, rite, 0)
            checks = []
            self.cache[rite] = midi.realtime.StreamPlayer(stream.Stream(note.Note(rite)))
            for colunm in range(1, self.count_but + 1):
                check = QCheckBox()
                check.setObjectName(f'{rite}')
                check.clicked.connect(self.clicked_note)
                self.gridLayout.addWidget(check, rite, colunm)
                checks += [check]
            self.all_checks[rite] += [*checks, ]

        self.YES.clicked.connect(self.save_melody)
        self.binding_checks()

    # восстановление мелодии, сохранённой при прошлом закрытии приложения
    def binding_checks(self):
        with open('settings_checks.txt', 'r', encoding='utf-8') as f:
            sp = f.readlines()
        for i in range(88):
            for j in range(self.count_but):
                if sp[i][j] == '1':
                    self.all_checks[i][j].setChecked(True)

    # воспроизведение звука ноты
    def clicked_note(self):
        if isinstance(self.sender(), QCheckBox) and not self.sender().isChecked():
            return
        name = int(self.sender().objectName())
        self.cache[name].play(blocked=False)

    # следующие 3 функции ныжны для сохранения мелодии при закрытии приложения
    def quit(self):
        sp = []
        for checks_in_rite in self.all_checks:
            s = ''
            for check in checks_in_rite:
                s += '1' if check.isChecked() else '0'
            s += '\n'
            sp += [s]
        with open('settings_checks.txt', 'w', encoding='utf-8') as f:
            f.writelines(sp)

    def exit_save_melody(self):
        for i in range(self.count_but):
            accord = chord.Chord()
            for j in range(88):
                check = self.all_checks[j][i]
                if check.isChecked():
                    accord.add(notes=note.Note(int(check.objectName())))
            self.melody += [accord]

    def save_melody(self):
        name = self.error.toPlainText()
        if name == '':
            self.error.setStyleSheet('QTextEdit{background-color:rgb(250,30,50); color: yellow;}')
            self.error.setText('ERROR! Вы не ввели имя файла для соxранения!')
        else:
            self.exit_save_melody()
            streaming = stream.Stream()
            for accord in self.melody:
                streaming.append(accord)
            streaming.write('midi', 'last_save_melody.midi')
            fs = FluidSynth()
            fs.midi_to_audio('last_save_melody.midi', name + '.wav')

    # воспроизведение текущей мелодии
    def play_a_melody(self):
        self.exit_save_melody()
        for accord in self.melody:
            midi.realtime.StreamPlayer(stream.Stream(accord)).play()

    # добавление клеточек для синтезатора
    def add_cells(self):
        count = int(self.count_cells.text())
        for rite in range(88):
            checks = []
            for colunm in range(1, count + 1):
                check = QCheckBox()
                check.setObjectName(f'{rite}')
                check.clicked.connect(self.clicked_note)
                self.gridLayout.addWidget(check, rite, colunm + self.count_but)
                checks += [check]
            self.all_checks[rite] += [*checks, ]
        self.count_but += count

    # очистка всех кнопок
    def delit_all(self):
        for checks_in_rite in self.all_checks:
            for check in checks_in_rite:
                check.setChecked(False)
