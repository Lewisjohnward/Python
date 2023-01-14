from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QVBoxLayout, QLabel

placeholder_txt = "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        menu_widget = QListWidget()


        placeholder_label = QLabel(placeholder_txt)
        button = QPushButton("Something")
        layoutb = QVBoxLayout()
        layoutb.addWidget(placeholder_label)
        layoutb.addWidget(button)

        layout = QHBoxLayout()

        for i in range (9):
            item = QListWidgetItem(f'{i}')
            item.setTextAlignment(Qt.AlignCenter)
            menu_widget.addItem(item)


        layout.addWidget(menu_widget, 1)
        layout.addLayout(layoutb, 4)
        self.setLayout(layout)


        self.show()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    with open("style.qss", "r") as f:
        _style = f.read()
        w.setStyleSheet(_style)
    app.exec()

