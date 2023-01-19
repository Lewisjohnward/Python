from PySide6.QtWidgets import *
from PySide6.QtCore import *

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.showUI()

    def showUI(self):
        w = QWidget()
        scroll_area = QScrollArea()
        l = QVBoxLayout()
        for i in range(100):
            label = QLabel("label")
            label.setStyleSheet("background: #AAAAAA")
            l.addWidget(label)

        w.setLayout(l)
        # Scroll area properties
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(w)


        self.setCentralWidget(scroll_area)
        self.show()

def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

