from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt 
from PySide6.QtGui import QFont 



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.f = open("binary.py", "rb").read()
        self.offset = 0

        byte = "04" 
        self.byte_label = QLabel()
        self.char = QLabel()
        self.char.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.char.setFont(QFont('Arial', 50))
        self.byte_label.setText(byte)
        self.byte_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.byte_label.setFont(QFont('Arial', 50))
        button = QPushButton("Next byte")
        button.clicked.connect(self.increment_offset)

        grid = QGridLayout()
        grid.addWidget(self.byte_label, 0, 0, 1, 1)
        grid.addWidget(self.char, 1, 0, 1, 1)
        grid.addWidget(button, 2, 0, 1, 1)
        self.setLayout(grid)

        self.show()

    def increment_offset(self):
        self.offset += 1
        self.byte_label.setText(str(self.f[self.offset]))
        self.char.setText(str(chr(self.f[self.offset])))






app = QApplication([])
window = MainWindow()
app.exec()



