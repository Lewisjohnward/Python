#!/usr/bin/python

"""
ZetCode PySide tutorial 

This program creates a menubar.

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
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setShortcut('q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Menubar')    
        self.show()
        
        
def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
