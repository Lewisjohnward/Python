import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.show()




def main():
    app = QApplication()
    ex = Example()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

