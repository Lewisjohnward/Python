from PySide6.QtWidgets import (QWidget, QApplication)
from PySide6.QtUiTools import QUiLoader


loader = QUiLoader()
app = QApplication([])


def do_something():
    print(window.fullname_line_edit.text(), "is a ", window.occupation_line_edit.text())

window = loader.load("widget.ui", None)
window.setWindowTitle("Window")
window.submit_button.clicked.connect(do_something)
window.show()
app.exec()
