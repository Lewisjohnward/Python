"""
    Displays a tooltip on both button & widget
"""


import sys
from PySide6.QtWidgets import QApplication, QWidget, QToolTip, QPushButton
from PySide6.QtGui import QFont


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        QToolTip.setFont(QFont('SansSerif', 50))
        self.setToolTip("This is a <b>joke</b>")
        
        btn = QPushButton("Button", self)
        btn.setToolTip("This is a button")
        btn.resize(btn.sizeHint())
        btn.move(50, 50)
        self.setGeometry(300, 300, 250, 150)


        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
