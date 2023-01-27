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

import sys
import os
import random

uncovered_colors = [
        "white",
        "#5f6ecf",
        "#e6ca4e",
        "#d4a168",
        "#b83428",
        "#8a28b8",
        "#b8283b"
        ]

class AnimatedHoverButton(QPushButton):
    def __init__(self, ismine, pos_x, pos_y, update_flags, start_game, end_game, grid_size):
        super().__init__()
        self.initUI()
        self.ismine = ismine
        self.flag = False
        self.update_flags = update_flags
        self.start_game = start_game
        self.uncovered = False
        self.end_game = end_game
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.grid_size = grid_size

    def initUI(self):
        self.setStyleSheet("border-top: 1px solid gray; border-right: 4px solid gray; border-bottom: 4px solid gray; border-left: 1px solid gray")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.animateHover = False

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            self.handle_right_click()
        elif e.button() == Qt.MouseButton.LeftButton and self.flag != True:
            self.handle_left_click()

    def handle_right_click(self):
        if self.uncovered:
            return
        if self.flag:
            self.setIcon(QIcon(""))
            self.flag = False
        else:
            self.flag = True
            self.setIcon(QIcon("./icons/red-flag.png"))
        self.update_flags(self.flag)
    

    def handle_left_click(self):
        if self.uncovered:
            return
        if self.ismine:
            self.setIcon(QIcon("./icons/nuclear-bomb.png"))
            self.end_game(True)
        else:
            self.uncover()

    def uncover(self):
        self.uncovered = True

        btn_list = self.parent().children()
        btn_list = btn_list[1:]

        def runcover(btn):
            x = btn.pos_x
            y = btn.pos_y

            coords = []
            coords.append([y - 1, x])
            coords.append([y + 1, x])
            coords.append([y , x + 1])
            coords.append([y , x - 1])

            for i,coord in enumerate(coords):
                if coord[0] < 0 or coord[1] < 0 or coord[0] > 9 or coord[1] > 9:
                    coords.pop(i)

            btn.uncovered = True


            for coord in coords:

                coord_y = coord[0] 
                coord_x = coord[1] * 10
                position_in_arr = coord_y + coord_x

                if btn_list[position_in_arr].ismine == False and btn_list[position_in_arr].uncovered == False:
                    runcover(btn_list[position_in_arr])

        runcover(self)
        self.display_touching()

    def display_touching(self):
        btn_list = self.parent().children()
        btn_list = btn_list[1:]
        uncovered_list = filter(lambda btn: btn.uncovered, btn_list)
        for uncovered in uncovered_list:
            touching = self.count_touching_bombs(uncovered)
            uncovered.setText(touching)
            uncovered.set_color(touching)



    def count_touching_bombs(self, uncovered):
        btn_list = self.parent().children()
        btn_list = btn_list[1:]
        touching = 0
        x = uncovered.pos_x
        y = uncovered.pos_y
        coords = []
        coords.append([y - 1, x])
        coords.append([y - 1, x - 1])
        coords.append([y - 1, x + 1])

        coords.append([y + 1, x])
        coords.append([y + 1, x - 1])
        coords.append([y + 1, x + 1])

        coords.append([y , x + 1])
        coords.append([y , x - 1])

        nlist = []
        for i,coord in enumerate(coords):
            if coord[0] >= 0 and coord[0] <= 9 and coord[1] >= 0 and coord[1] <= 9:
                nlist.append(coord)

        coords = nlist

        for coord in coords:
            coord_y = coord[0] 
            coord_x = coord[1] * 10
            position_in_arr = coord_y + coord_x

            if btn_list[position_in_arr].ismine == True:
                touching += 1

        if touching == 0:
            return ""
        else:
            return str(touching)

    def restart(self):
        print("restart")

    def choose_random_start(self):
        btn_list = self.parent().children()[1:]
        safe_areas = list(filter(lambda btn: btn.ismine == False, btn_list))
        random_btn = random.choice(safe_areas)
        random_btn.uncover()

    def set_color(self, adjacent):
        index = int(adjacent)
        self.setStyleSheet(f"color: {uncovered_colors[index]}; background: darkgray")


class Header(QHBoxLayout):
    def __init__(self, restart_game):
        super().__init__()

        self.remaining_flags = 99
        self.counter = 0
        self.restart_game = restart_game

        style = "font-family: FreeMono; font-size: 20px; color: red; font-weight: bold; padding: 4px; border: 1px solid black; background: black"


        self.flag_count = QLabel("099")
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


class Grid(QWidget):
    def __init__(self, update_flags, start_game, end_game):
        super().__init__()
        self.update_flags = update_flags
        self.start_game = start_game
        self.end_game = end_game

        mines = list() 
        self.grid = QGridLayout()

        for j in range(10):
            sublist = list()
            for i in range(10):
                sublist.append(random.randint(0, 1))
            mines.append(sublist)
            sublist = []


        self.grid_count = 10

        for i in range(self.grid_count):
            for j in range(self.grid_count):
                self.btn = AnimatedHoverButton(mines[i][j], i, j, self.update_flags, self.start_game, self.end_game, self.grid)
                self.grid.addWidget(self.btn, i, j, 1, 1)

        self.setLayout(self.grid)
        self.setStyleSheet("border: 1px solid black;")

    def mousePressEvent(self, e):
        print("hello")
        #self.clicked.connect(lambda : print("hello"))


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

