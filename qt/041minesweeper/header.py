from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class Header(QHBoxLayout):
    def __init__(self, restart_game):
        super().__init__()

        self.remaining_flags = 99
        self.counter = 0
        self.restart_game = restart_game

        style = "font-family: FreeMono; font-size: 20px; color: red; font-weight: bold; padding: 4px; border: 1px solid black; background: black"


        #self.flag_count = QLabel("099")
        self.flag_count = QLCDNumber()
        self.flag_count.setStyleSheet(style)
        self.restart_button = QPushButton()
        self.restart_button.setIcon(QIcon("./icons/happiness.png"))
        self.restart_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.restart_button.setMaximumSize(40, 40)
        self.restart_button.clicked.connect(self.restart_game)
        self.timer = QLabel("00")
        self.timer.setStyleSheet(style)

        self.addWidget(self.flag_count)
        self.addStretch()
        self.addWidget(self.restart_button)
        self.addStretch()
        self.addWidget(self.timer)

    def update_flags(self, adding_flag):
        if adding_flag:
            self.remaining_flags -= 1
        else:
            self.remaining_flags += 1
        self.flag_count.setText(str(self.remaining_flags))

    def increment_counter(self):
        self.counter += 1
        self.timer.setText(str(self.counter))

    def end_game(self, dead):
        if dead:
            self.restart_button.setIcon(QIcon("./icons/sad.png"))

    def restart(self):
        self.counter = 0
        self.timer.setText(str(self.counter))
        self.remaining_flags = 99
        self.flag_count.setText(str(self.remaining_flags))


