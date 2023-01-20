import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
import struct


class Button(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

class Counter(QLabel):
    def __init__(self):
        super().__init__()
        self.count = 0

        self.setText(str(self.count))
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 55px")

    def modify(self, quantity):
        self.count += quantity
        self.setText(str(self.count))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        w = QWidget()
        l = QHBoxLayout()
        self.count = Counter()
        inc_button = Button("+")
        inc_button.clicked.connect(lambda : self.count.modify(1))
        dec_button = Button("-")
        dec_button.clicked.connect(lambda: self.count.modify(-1))
        l.addWidget(dec_button)
        l.addWidget(self.count)
        l.addWidget(inc_button)
        w.setLayout(l)
        self.setCentralWidget(w)

        self.show()


def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec()) 


if __name__ == "__main__":
    main()

    
