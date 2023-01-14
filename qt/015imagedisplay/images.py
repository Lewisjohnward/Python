from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QLabel, QVBoxLayout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QLabel Image Demo")
        image_label = QLabel()
        image_label.setPixmap(QPixmap("./2022-05-22_18-49.png"))
        v_layout = QVBoxLayout()
        v_layout.addWidget(image_label)

        self.setLayout(v_layout)

        


        self.show()



app = QApplication([])
window = MainWindow()
app.exec()
