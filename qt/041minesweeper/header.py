from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class LCDDisplay(QLCDNumber):
    def __init__(self):
        super().__init__()
        #self.display(count)
        self.setProperty("class", "lcd")




class Smiley(QPushButton):
    def __init__(self, path):
        super().__init__()
        self.setIcon(QIcon(path))
        self.setProperty("class", "btn inverseBorder")
        self.setMinimumWidth(40)
        self.setMinimumHeight(40)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class HeaderUI(QFrame):
    def __init__(self):
        super().__init__()

        self.setProperty("class", "header border")
        self.flags = FlagCount(99)
        self.timer = Timer(0)
        self.smiley = Smiley("./icons/happiness.png")


        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.flags)
        layout.addStretch()
        layout.addWidget(self.smiley)
        layout.addStretch()
        layout.addWidget(self.timer)
        self.setMinimumHeight(65)
        self.setLayout(layout)


################## LOGIC ###########

class FlagCount(LCDDisplay):
    def __init__(self, count):
        super().__init__()
        self.count = count
        self.init_display()

    def init_display(self):
        self.display(self.count)

    def decrement_flag(self):
        if self.count >= 0:
            self.count -= 1
            self.display(self.count)

    def increment_flag(self):
        if self.count < 99:
            self.count += 1
            self.display(self.count)

    def finished_flags(self):
        if self.count == 0:
            return True
        else:
            return False
    def reset_flags(self):
        self.display(99)

        

class Timer(LCDDisplay):
    def __init__(self, count):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.increment_time)
        self.count = count
        self.init_display()

    def init_display(self):
        self.display(self.count)

    def increment_time(self):
        self.count += 1
        self.display(self.count)

    def start_timer(self):
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.count = 0
        self.display(self.count)

class Header(HeaderUI):
    def __init__(self, restart_game):
        super().__init__()
        self.restart_game = restart_game
        self.smiley.clicked.connect(self.restart_game)


