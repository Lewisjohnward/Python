from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        label = QLabel("Hello world")
        label.setStyleSheet("font-size: 25px;")
        label.setAlignment(Qt.AlignRight | Qt.AlignTop)
        layout = QHBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

        self.show()


app = QApplication([])
window = MainWindow()
app.exec()
