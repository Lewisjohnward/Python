"""
    Creating a quit button that quits using QCoreApplication
"""

import sys
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication, QPushButton, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_UI()

    def init_UI(self):
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)
        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())
