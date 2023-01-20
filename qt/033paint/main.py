"""
    A paint app where the user draws using the mouse
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QPainter, QBrush, QColor, QPen, QIcon
from PySide6.QtCore import Qt, QSize

COLORS = [
# 17 undertones https://lospec.com/palette-list/17undertones
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

class QPaletteButton(QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QSize(24,24))
        self.setStyleSheet("background-color: %s;" % color)

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(2000, 1800)
        pixmap.fill(Qt.white)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QColor('#000000')

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        x = e.pos().x()
        y = e.pos().y() + 400

        if self.last_x is None:
            self.last_x = x
            self.last_y = y
            return

        canvas = self.pixmap()
        painter = QPainter(canvas)
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, x, y)
        painter.end()
        self.setPixmap(canvas)

        # Update the origin for next time.
        self.last_x = x
        self.last_y = y

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.color = "#eb4034"

    def initUI(self):
        self.canvas = Canvas()
        w = QWidget()
        l = QVBoxLayout()

        w.setLayout(l)
        l.addWidget(self.canvas)

        palette = QHBoxLayout()
        self.add_palette_buttons(palette)
        l.addLayout(palette)
        self.setCentralWidget(w)


        self.show()

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)
        spray_button = QPushButton()
        spray_button.setIcon(QIcon("./icons/spray.png"))
        spray_button.setFixedSize(QSize(24, 24))
        layout.addWidget(spray_button)



def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

