"""
    A very ugly random number generator built using Qt
"""

import sys
import random

from PyQt5.QtWidgets import (
        QMainWindow,
        QApplication,
        QLabel,
        QWidget,
        QPushButton,
        QVBoxLayout
)

nums = [
        1,
        2,
        3,
        4,
        5,
        6
    ]

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

    
        window = QWidget()
        window.setGeometry(0, 0, 100, 100)

        container = QVBoxLayout()
        self.widget = QLabel("Press to generate number")
        font = self.widget.font()
        font.setPointSize(30)
        self.widget.setFont(font)

        button_generate_num = QPushButton("Gen number")
        button_generate_num.clicked.connect(self.update_num)

        container.addWidget(button_generate_num)
        container.addWidget(self.widget)

        window.setLayout(container)

        self.setCentralWidget(window)
        
    def update_num(self):
        self.widget.setText(str(random.choice(nums)))




app = QApplication([])
window = MainWindow()
window.show()
app.exec()

