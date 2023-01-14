from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel


class MainWindow(QLabel):
    def __init__(self):
        super().__init__()

        self.setText("Placeholder text")
        self.setAlignment(Qt.AlignCenter)

        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    with open("style.qss", "r") as f:
            _style = f.read()
            app.setStyleSheet(_style)

    app.exec()


