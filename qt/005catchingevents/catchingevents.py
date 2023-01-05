"""
Handling events

Widgets act as event-catchers. This means that every widget can catch specific events
like mouse clicks, keypresses, and so on. In response to these events, 
a widget emits a signal, which is a kind of message that announces a change in its state

If a signal is connected to a slot, then the slot is called whenever the signal is emitted. 
If a signal isn't connected to any slot, then nothing happens and the signal is ignored. 

A signal can be connected to one or many slots
A signal may also be connected to another signal
A slot may be connected to one or many signals

The following syntax is used to connect a signal and a slot:
    widget.signal.connect(slot_function)

whenever .signal is emmited, slot_function() will be called
"""

import sys


from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

def greet():
    if msgLabel.text():
        msgLabel.setText("")
    else:
        msgLabel.setText("Hello, World!")

app = QApplication([])
window = QWidget()
window.setWindowTitle("Signals and slots")
layout = QVBoxLayout()

button = QPushButton("Greet")
button.clicked.connect(greet)

layout.addWidget(button)
msgLabel = QLabel("")
layout.addWidget(msgLabel)
window.setLayout(layout)
window.show()
sys.exit(app.exec())


