"""
    A look at Qt's API for performing pitmap graphic operations and the basis 
    for drawing your own widgets
"""


import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from random import randint, choice
from time import sleep



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel()
        canvas = QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        #self.draw_line()
        #self.draw_pixel()
        #self.draw_styled_pixel()
        #self.draw_multiple_pixels()
        self.draw_multiple_multicolored_pixels()
        self.show()

    def draw_multiple_multicolored_pixels(self):
        colors = ['#FFD141', '#376F9F', '#0D1F2D', '#E9EBEF', '#EB5160']

        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)

        for n in range(10000):
            # pen = painter.pen() you could get the active pen here
            pen.setColor(QColor(choice(colors)))
            painter.setPen(pen)
            painter.drawPoint(
                200+randint(-100, 100),  # x
                150+randint(-100, 100)   # y
                )
        painter.end()
        self.label.setPixmap(canvas)

    def draw_multiple_pixels(self):
        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        # default pen 3pixel width and black
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)

        for n in range(10000):
            painter.drawPoint(
                    200+randint(-100, 100),
                    150+randint(-100, 100)
                    )
        painter.end()
        self.label.setPixmap(canvas)

    def draw_styled_pixel(self):
        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        pen = QPen()
        # Sets pen width to 40
        pen.setWidth(40)
        # Sets pen color to red
        pen.setColor(QColor('red'))
        # Sets painter to pen
        painter.setPen(pen)
        painter.drawPoint(200, 150)
        painter.end()
        self.label.setPixmap(canvas)

    def draw_pixel(self):
        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        # Draws a point at 200, 150
        painter.drawPoint(200, 150)
        painter.end()
        self.label.setPixmap(canvas)

    def draw_line(self):
        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        #draws a line from 0, 0 to 400, 300
        painter.drawLine(0, 0, 400, 300)
        painter.end()
        self.label.setPixmap(canvas)

def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
