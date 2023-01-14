import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        horiz_layout = QHBoxLayout()
        horiz_layout.addStretch()
        horiz_layout.addWidget(ok_button)
        horiz_layout.addWidget(cancel_button)
        vertical_layout = QVBoxLayout()
        vertical_layout.addStretch()
        vertical_layout.addLayout(horiz_layout)
        self.setLayout(vertical_layout)
        self.show()


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
