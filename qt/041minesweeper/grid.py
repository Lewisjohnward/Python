from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

from random import randint, shuffle, choice

##### UI ####################
class AnimatedHoverButtonUI(QPushButton):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setProperty("class", "btn inverseBorder")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class GridUI(QFrame):
    def __init__(self, grid_count = 10):
        super().__init__()
        self.grid_count = grid_count
        self.initUI()

    def initUI(self):
        self.setProperty("class", "frame border")
        self.grid = QGridLayout()
        self.grid.setSpacing(0)
        self.grid.setContentsMargins(0, 0, 0, 0)

        mines = self.generateMines(45)

        for i in range(self.grid_count):
            for j in range(self.grid_count):
                self.btn = AnimatedHoverButton(mines[i][j], i, j)
                self.grid.addWidget(self.btn, i, j, 1, 1)

        self.setLayout(self.grid)

    # Generates the mines grid
    def generateMines(self, minesToPlace):
        seedMines = list() 
        numOfMines = minesToPlace
        for j in range(10):
            for i in range(10):
                if numOfMines > 0:
                    numOfMines -= 1
                    seedMines.append(1)
                else:
                    seedMines.append(0)
        shuffle(seedMines)
        mines = list()
        for i in range(10):
            mines.append(seedMines[i * 10: (i + 1) * 10])
        return mines

####### LOGIC ############################## 

class AnimatedHoverButton(AnimatedHoverButtonUI):
    def __init__(self, mine, pos_x, pos_y):
        super().__init__()
        self.mine = mine
        self.flag = False
        self.uncovered = False
        self.pos_x = pos_x
        self.pos_y = pos_y

    def mousePressEvent(self, e):
        # If game end don't accept clicks
        if self.parent().game_end or self.uncovered:
            return
        elif e.button() == Qt.MouseButton.LeftButton and not self.flag:
            self.click_handle()
        elif e.button() == Qt.MouseButton.RightButton:
            self.place_flag()

    def place_flag(self):
        if self.flag:
            self.flag = False
            self.remove_flag()
            self.parent().header.flags.increment_flag()
            return
        else:
            self.setIcon(QIcon("./icons/red-flag.png"))
            self.parent().header.flags.decrement_flag()
            self.flag = True

    def remove_flag(self):
            self.setIcon(QIcon(""))

    def click_handle(self):
        if self.parent().first_selection:
            self.mine = False
            self.parent().first_selection = False
            self.uncover_space()
            self.parent().parent().parent().start_game()
        else:
            self.uncover_space()

    def uncover_space(self):
        if self.mine:
            self.parent().parent().parent().restart_game()
        else:
            self.uncover()

        if self.uncovered_all_spaces():
            self.parent().parent().parent().won_game()

    def uncovered_all_spaces(self):
        for i, btn in enumerate(self.parent().children()):
            if i == 0:
                continue
            if not btn.mine and not btn.uncovered:
                return False
        return True


    def refresh_style(self):
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mark_uncovered(self):
        self.uncovered = True
        self.remove_flag()
        self.setProperty("class", "uncoveredSafe")
        self.refresh_style()

    def uncover_end(self):
        if self.mine:
            ### END GAME LOGIC HERE
            self.setProperty("class", "uncoveredBomb")
            self.setIcon(QIcon("./icons/bomb.png"))
            self.refresh_style()
        else:
            self.setProperty("class", "uncoveredSafe")
            self.setText("")
            self.refresh_style()


    def uncover(self):
        self.mark_uncovered()
        btn_list = self.parent().children()[1:]

        def uncover_adjacent(btn):
            btn.mark_uncovered()
            x = btn.pos_x
            y = btn.pos_y

            coords = []
            coords.append([y - 1, x])
            coords.append([y + 1, x])
            coords.append([y , x + 1])
            coords.append([y , x - 1])
            tmp = []


            for i in coords:
                if i[0] >= 0 and i[0] <= 9 and i[1] >=0 and i[1] <= 9:
                    tmp.append(i)
            coords = tmp

            for coord in coords:

                coord_y = coord[0] 
                coord_x = coord[1] * 10
                position_in_arr = coord_y + coord_x

                if btn_list[position_in_arr].mine == False and btn_list[position_in_arr].uncovered == False:
                    uncover_adjacent(btn_list[position_in_arr])

        uncover_adjacent(self)
        self.display_touching()

    def display_touching(self):
        btn_list = self.parent().children()
        btn_list = btn_list[1:]
        uncovered_list = filter(lambda btn: btn.uncovered, btn_list)
        for uncovered in uncovered_list:
            touching = self.count_touching_bombs(uncovered)
            uncovered.setText(touching)
            uncovered.set_color(touching)

    def set_color(self, touching):
        colors = [
                "#0091ff",
                "#34eb6e",
                "#bdeb34",
                "#b037ed",
                "#ed3737",
                "#f00a0a",
                "#fa0505",
                "#080808"
                ]

        i = 0
        try:
            i = int(touching)
        except ValueError:
            pass
        if i == 0:
            return
        self.setStyleSheet(f'color: {colors[i - 1]};')

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

            if btn_list[position_in_arr].mine == True:
                touching += 1

        if touching == 0:
            return ""
        else:
            return str(touching)

class Grid(GridUI):
    def __init__(self, header):
        super().__init__()
        self.header = header
        self.first_selection = True
        self.game_end = False


    def uncover_all(self):
        for i, space in enumerate(self.children()):
            if not i:
                continue
            else:
                space.uncover_end()
        self.game_end = True
