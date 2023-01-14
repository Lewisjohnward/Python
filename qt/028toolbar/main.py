#!/usr/bin/python

"""
ZetCode PySide tutorial 

This program creates a toolbar.

author: Jan Bodnar
website: zetcode.com
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction, QIcon

class Example(QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        
        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Toolbar')    
        self.show()
        
        
def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
