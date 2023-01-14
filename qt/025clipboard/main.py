"""
    A look at clipboard functionality
    https://doc.qt.io/qt-6/qclipboard.html
"""
import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QGuiApplication

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        clipboard = QGuiApplication.clipboard()
        #changed signals when user highlights data
        clipboard.changed.connect(self.clipboardChanged)
        #datachanges signals when user adds to clipboard
        clipboard.dataChanged.connect(self.clipboardDataChanged)
        #findBufferChanged signals when
        clipboard.findBufferChanged.connect(self.clipboardFindBufferChanged)
        clipboard.selectionChanged.connect(self.clipboardSelectionChanged)
        self.show()


    def clipboardChanged(self):
        print("Clipboard changed")

    def clipboardDataChanged(self):
        print("Clipboard data changed")

    def clipboardFindBufferChanged(self):
        print("Clipboard find data buffer changed")

    def clipboardSelectionChanged(self):
        print("Clipboard selection changed")






def main():
    app = QApplication([])
    w = MainWindow()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()




