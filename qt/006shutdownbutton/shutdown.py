"""
    GUI with buttons to shutdown/restart system
"""

import sys
import os

from PyQt5.QtWidgets import (
        QApplication,
        QLabel,
        QPushButton,
        QVBoxLayout,
        QWidget
)


def shutdown():
    os.system("shutdown now")

def restart():
    os.system("shutdown -r now")

app = QApplication([])
window = QWidget()
window.setWindowTitle("Shutdown System")
layout = QVBoxLayout()

button_shutdown = QPushButton("Shutdown")
button_shutdown.clicked.connect(shutdown)

button_restart = QPushButton("Restart")
button_restart.clicked.connect(restart)

layout.addWidget(button_shutdown)
layout.addWidget(button_restart)

msgLabel = QLabel("")
layout.addWidget(msgLabel)
window.setLayout(layout)
window.show()
sys.exit(app.exec())
