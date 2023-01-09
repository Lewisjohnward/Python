"""
    A program that prints a random quote with a random font style
"""

from random import randint
from assets import (fonts, quotes)
from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
        QLabel,
        QPushButton,
        QHBoxLayout,
        QVBoxLayout,
        QWidget
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addStretch()
        self.label = QLabel("Sample text")
        self.label.setFont(QFont('Arial', 50))
        horizontal_layout.addWidget(self.label)
        horizontal_layout.addStretch()
        vertical = QVBoxLayout()
        vertical.addStretch()
        vertical.addLayout(horizontal_layout)
        horizontal_layout2 = QHBoxLayout()
        horizontal_layout2.addStretch()
        button = QPushButton("Change font")
        button.clicked.connect(self.change_font)
        horizontal_layout2.addWidget(button)
        horizontal_layout2.addStretch()
        vertical.addLayout(horizontal_layout2)
        vertical.addStretch()
        self.setLayout(vertical)


    def change_font(self):
        self.label.setText(quotes[randint(0, len(quotes) - 1)])
        self.label.setFont(QFont(fonts[randint(0, len(fonts) - 1)], 10))


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
