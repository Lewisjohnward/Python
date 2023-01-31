"""
    Minesweeper game in a dialog widget
    To do:
        Add random start
        Reduce number of mines
        Put grid in its own class
        Win game ending
        Add animation to uncovering safe spots
"""

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from header import Header
from grid import Grid

import sys



class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.started = False
        self.dead = False
        self.won = False

        self.initUI()

    def initUI(self):
        self.resize(400, 400)
        vert_layout = QVBoxLayout()
        # Header
        self.header = Header(self.restart_game)

        grid = Grid(self.header.update_flags, self.start_game, self.end_game)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.header.increment_counter)

        vert_layout.addLayout(self.header)
        vert_layout.addWidget(grid, 2)


        self.setLayout(vert_layout)
        self.show()

    def end_game(self, dead):
        self.timer.stop()
        self.header.end_game(dead)

    def start_game(self):
        if self.started == False:
            print("starting game")
            self.started = True
            self.increment_time()

    def increment_time(self):
        if self.started == True:
            self.header.increment_counter()
            self.timer.start(1000)
        if self.started == False:
            self.timer.stop()

    def restart_game(self):
        self.header.restart()
        self.btn.restart()
        self.timer.stop()
        self.started = False


def main():
    app = QApplication([])
    w = Dialog()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

