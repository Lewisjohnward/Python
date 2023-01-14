from PyQt5.QtWidgets import (QMainWindow, QWidget, QApplication, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout) 

from PyQt5.QtGui import QClipboard

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Creating the buttons
        randomtxt = QPushButton("Random text")
        randomtxt.clicked.connect(self.random)
        copy = QPushButton("Copy")
        copy.clicked.connect(self.copy)
        cut = QPushButton("Cut")
        cut.clicked.connect(self.cut)
        paste = QPushButton("Paste")
        paste.clicked.connect(self.paste)
        undo = QPushButton("Undo")
        undo.clicked.connect(self.undo)
        html = QPushButton("Set html")
        html.clicked.connect(self.html)
        clear = QPushButton("Clear")
        clear.clicked.connect(self.clear)

        # Adding the buttons to bar
        topbar = QHBoxLayout()
        topbar.addWidget(randomtxt)
        topbar.addWidget(clear)
        topbar.addWidget(copy)
        topbar.addWidget(cut)
        topbar.addWidget(paste)
        topbar.addWidget(undo)
        topbar.addWidget(html)


        page = QVBoxLayout()
        page.addLayout(topbar)

        self.textbox = QTextEdit()
        page.addWidget(self.textbox)

        window = QWidget()
        window.setLayout(page)

        self.setCentralWidget(window)



    def html(self):
        print("html")

    def undo(self):
        self.textbox.undo()

    def paste(self):
        # Append text from clipboard
        clipboard = QApplication.clipboard()
        current = self.textbox.toPlainText()
        self.textbox.setText(current + clipboard.text())

    def cut(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textbox.toPlainText())

    def copy(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.textbox.toPlainText())


    def random(self):
        self.textbox.setText("asdf;asldfjas;dflhkasdl;kfhjasdlkfhjasdlfkjh")

    def clear(self):
        self.textbox.setText("")



        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
