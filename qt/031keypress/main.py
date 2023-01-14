#!/usr/bin/python

"""
In this example, we reimplement an 
event handler. 

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6 import QtCore

class Example(QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()
        
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        
def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
