"""
    A paint app where the user draws using the mouse
"""


import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.label = QLabel()
        canvas = QPixmap(400, 300)
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        self.last_x, self.last_y = None, None
        self.show()

    def mouseMoveEvent(self, e):
        p = e.globalPosition()
        globalPos = p.toPoint()
        x = globalPos.x() - 1237
        y = globalPos.y() - 397

        if self.last_x is None:
            self.last_x = x
            self.last_y = y
            return

        canvas = self.label.pixmap()
        painter = QPainter(canvas)
        painter.drawLine(self.last_x, self.last_y, x, y)
        painter.end()
        self.label.setPixmap(canvas)

        self.last_x = x
        self.last_y = y

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.lasy_y = None






def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

