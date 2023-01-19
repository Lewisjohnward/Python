from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import os
import sys
import getpass
import uuid

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        w = QWidget()
        l = QHBoxLayout()
        btn = QPushButton("REMOVE ME")
        btn.setMinimumSize(200, 200)
        btn.setStyleSheet("border: 1px solid black;")
        btn.clicked.connect(lambda : btn.deleteLater())

        btn.setSizePolicy(QSizePolicy.Fixed , QSizePolicy.Fixed)
        l.addWidget(btn)
        w.setLayout(l)

        self.setCentralWidget(w)
        self.show()

def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
