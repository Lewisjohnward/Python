from PyQt5.QtCore import QSize

from PyQt5.QtWidgets import (QApplication, QGridLayout, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        letter = QLabel("?")

        main = QVBoxLayout()
        main.addWidget(letter)
        grid = QGridLayout()

        pushButton_b1 = QPushButton("A")
        pushButton_b2 = QPushButton("B")
        pushButton_b3 = QPushButton("C")
        pushButton_b4 = QPushButton("D")
        pushButton_b5 = QPushButton("E")
        pushButton_b6 = QPushButton("F")
        pushButton_b7 = QPushButton("G")
        pushButton_b8 = QPushButton("H")
        pushButton_b9 = QPushButton("I")

        grid.addWidget(pushButton_b1, 0, 0, 1, 1)
        grid.addWidget(pushButton_b2, 0, 1, 1, 1)
        grid.addWidget(pushButton_b3, 0, 2, 1, 1)
        grid.addWidget(pushButton_b4, 1, 0, 1, 1)
        grid.addWidget(pushButton_b5, 1, 1, 1, 1)
        grid.addWidget(pushButton_b6, 1, 2, 1, 1)
        grid.addWidget(pushButton_b7, 2, 0, 1, 1)
        grid.addWidget(pushButton_b8, 2, 1, 1, 1)
        grid.addWidget(pushButton_b9, 2, 2, 1, 1)


        main.addLayout(grid)
        self.setLayout(main)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()


