from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

import os
import sys
import getpass
import uuid

class Clipping():
    def __init__(self, title, text):
        key = uuid.uuid4()
        self.key = key
        self.title = title
        self.text = text

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.txt = []
        self.initUI()
    def initUI(self):

        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+q')
        exitAction.setShortcut('q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openAction = QAction(QIcon('load.png'), '&Load', self)
        openAction.setShortcut('Ctrl+o')
        openAction.setShortcut('o')
        openAction.setStatusTip('Load clippings')
        #openAction.setEnabled(False)
        openAction.triggered.connect(self.load)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        

        self.l = QVBoxLayout()
        w = QWidget()
        w.setLayout(self.l)
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(w)

        self.setCentralWidget(self.scroll_area)

        self.show()

    def load(self):
        user = getpass.getuser() 
        directory = f'/media/{user}/Kindle/documents/'
        #filename, _ = QFileDialog.getOpenFileName(self, "Open file", directory, "Txt file (*.txt);;""All files (*.*)")
        filename = f'/media/{user}/Kindle/documents/My Clippings.txt'
        if filename:
            try:
                with open(filename, "r") as f:
                    tmp = f.read().split("\n")
                    while len(tmp) > 0:
                        try:
                            raw_clipping = tmp[:5]
                            if len(raw_clipping[3]) != 0:
                                title = raw_clipping[0]
                                new_clipping = Clipping(title, raw_clipping[3])
                                self.txt.append(new_clipping)
                            del tmp[:5]
                        except:
                            break
            except IOError:
                print("Unable to open file")
        self.updateUI()

    def updateUI(self):
        for clipping in self.txt:
            key = clipping.key
            title = QLineEdit(clipping.title)
            title.setCursorPosition(0)
            title.setMaximumWidth(100)
            text = QLineEdit(clipping.text)
            text.setCursorPosition(0)
            delete_btn = QPushButton("X")
            delete_btn.setMaximumWidth(10)
            h = QHBoxLayout()
            h.addWidget(title)
            h.addWidget(text)
            h.addWidget(delete_btn)
            self.l.addLayout(h)
            delete_btn.pressed.connect(lambda key=key, h=h: self.remove_clipping(key, h))

    def remove_clipping(self, key, layout):
        for i, o in enumerate(self.txt):
            if o.key == key:
                del self.txt[i]
                break

        while layout.count():
            child = layout.takeAt(0)
            parent = layout.parent()
            if child.widget():
                child.widget().setParent(None)


def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
