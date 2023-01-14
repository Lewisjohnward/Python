from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QTimeEdit, QVBoxLayout, QLineEdit, QHBoxLayout



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.count = 0
        self.counter = QLineEdit(str(self.count))

        inc_button = QPushButton("+")
        inc_button.clicked.connect(self.increment)
        dec_button = QPushButton("-")
        dec_button.clicked.connect(self.decrement)

        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        hlayout.addWidget(dec_button)
        hlayout.addWidget(self.counter)
        hlayout.addWidget(inc_button)

        self.setLayout(hlayout)

        self.show()

    def increment(self):
        self.count += 1
        self.counter.setText(str(self.count))

    def decrement(self):
        self.count -= 1
        self.counter.setText(str(self.count))
        






app = QApplication([])
window = MainWindow()
app.exec()
