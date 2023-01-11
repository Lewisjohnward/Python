from PyQt5.QtWidgets import (
        QApplication,
        QMainWindow,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()



app = QApplication([])
window = MainWindow()
window.show()
app.exec()
