"""
    A dialogue button with a button that when pressed shutsdown system
"""

import sys
import os

from PyQt5.QtWidgets import (
        QApplication,
        QDialog,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget
)


def shutdown():
    os.system("shutdown now")

app = QApplication([])
window = QWidget()
window.setWindowTitle("Shutdown System")
layout = QVBoxLayout()

button = QPushButton("Shutdown")
button.clicked.connect(shutdown)

layout.addWidget(button)
msgLabel = QLabel("")
layout.addWidget(msgLabel)
window.setLayout(layout)
window.show()
sys.exit(app.exec())
