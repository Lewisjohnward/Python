"""
    Minesweeper game in a dialog widget
"""


from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import sys
import os
import random

class AnimatedHoverButton(QPushButton):
    def __init__(self, ismine):
        super().__init__()
        self.initUI()
        self.ismine = ismine
        self.clicked.connect(self.handle_click)


    def initUI(self):
        self.setStyleSheet("border-top: 1px solid gray; border-right: 4px solid gray; border-bottom: 4px solid gray; border-left: 1px solid gray")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.animateHover = False

    def handle_click(self):
        if self.ismine:
            self.setIcon(QIcon("./icons/arrow-circle-225-left.png"))




class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.resize(400, 400)
        vert_layout = QVBoxLayout()
        # Header
        flag_count = QLabel("099")
        restart_button = QPushButton()
        restart_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        restart_button.setMaximumSize(40, 40)
        timer = QLabel("00")

        header_layout = QHBoxLayout()
        header_layout.addWidget(timer)
        header_layout.addStretch()
        header_layout.addWidget(restart_button)
        header_layout.addStretch()
        header_layout.addWidget(flag_count)
        ###

        widget = QWidget()
        mine_grid = QGridLayout()
        widget.setLayout(mine_grid)
        widget.setStyleSheet("border: 1px solid black;")

        mines = list() 
        for j in range(10):
            sublist = list()
            for i in range(10):
                sublist.append(random.randint(0, 1))
            mines.append(sublist)
            sublist = []


        grid = 10

        for i in range(grid):
            for j in range(grid):
                btn = AnimatedHoverButton(mines[i][j])
                mine_grid.addWidget(btn, i, j, 1, 1)


        

        vert_layout.addLayout(header_layout)
        vert_layout.addWidget(widget, 2)




        #w = QWidget()
        #button = QPushButton()
        #button.setIcon(QPixmap("./icons/arrow-circle-225-left.png"))
        #l = QHBoxLayout()
        #l.addWidget(w)
        #l.addWidget(button)

        self.setLayout(vert_layout)
        self.show()


def main():
    app = QApplication([])
    w = Dialog()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

