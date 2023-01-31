""" 
    Minesweeper
    python3 minesweeper.py
"""

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sys
from header import *
from grid import *

##### UI #######################

class EndgameDialogUI(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Congratulations you have finished the game")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "menubar")
        gameMenu = self.addMenu("&Game")
        self.addMenu("&Help")

        tempAction = QAction("&Exit", self)
        gameMenu.addAction(tempAction)


class MainWindowUI(QDialog):
    def __init__(self):
        super().__init__()
        f = open("./styles.qss")
        styles = f.read()

        self.header = Header(self.restart_game)
        self.grid = Grid(self.header)

        self.menu = MenuBar()

        self.vl = QVBoxLayout()
        self.vl.setSpacing(0)
        self.vl.setContentsMargins(0, 0, 0, 0)

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 0)
        self.vlayout.setSpacing(0)
        self.vl.addWidget(self.menu)
        self.vlayout.addWidget(self.header)
        self.vlayout.addWidget(self.grid)
        self.frame = QFrame()
        self.frame.setProperty("class", "mainframe")
        self.frame.setLayout(self.vlayout)
        self.vl.addWidget(self.frame)
        self.setProperty("class", "dialogBorder")
        self.setStyleSheet(styles)

        self.resize(500, 500)
        self.setLayout(self.vl)


        self.show()

################# Logic ###

class EndgameDialog(EndgameDialogUI):
    def __init__(self):
        super().__init__()

class MainWindow(MainWindowUI):
    def __init__(self):
        super().__init__()
        self.recreate_grid = False

    # Deletes the grid and redraws it
    def restart_game(self):
        if self.recreate_grid:
            self.grid.deleteLater()
            self.grid = Grid(self.header)
            self.vlayout.addWidget(self.grid)
            self.header.timer.reset_timer()
            self.recreate_grid = False
            self.header.flags.reset_flags()
        else:
            self.header.timer.stop_timer()
            self.grid.uncover_all()
            self.recreate_grid = True

    def start_game(self):
        self.header.timer.start_timer()

    def won_game(self):
        self.header.timer.stop_timer()
        dlg = EndgameDialog()
        dlg.exec()
        self.recreate_grid = True
        self.restart_game()


def main():
    a = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(a.exec())

if __name__ == "__main__":
    main()
