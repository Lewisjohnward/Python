from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from header import Header

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
        self.setStyleSheet("border-top: 3px solid white; border-right: 4px solid gray; border-bottom: 4px solid gray; border-left: 3px solid white")
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


class Grid(QWidget):
    def __init__(self, update_flags, start_game, end_game):
        super().__init__()
        self.update_flags = update_flags
        self.start_game = start_game
        self.end_game = end_game

        mines = list() 
        self.grid = QGridLayout()
        self.grid.setSpacing(0)

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
        self.setStyleSheet("border: 1px solid gray;")

    def mousePressEvent(self, e):
        print("hello")
