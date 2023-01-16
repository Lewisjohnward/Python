#!/usr/bin/python

"""
In this example, we reimplement an 
event handler. 

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PySide6 import QtCore
import struct 

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        layout = QHBoxLayout()
        self.key_label = QLabel("?")
        self.key_label.setAlignment(QtCore.Qt.AlignCenter)
        self.key_label.setStyleSheet("font-family: Titillium; font-size: 30px;")
        layout.addWidget(self.key_label)
        self.setLayout(layout)
        self.setWindowTitle('Event handler')
        self.show()
        
    def keyPressEvent(self, e):
        self.key_label.setText(str(e.key()))
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        
def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
