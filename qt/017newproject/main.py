from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QAbstractItemView, QLabel, QComboBox, QListWidgetItem


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        background = "#333333"
        font = "white"
        border = "1px solid #aaaaaa"
        background_select = "#3483eb"

        list_style = "QListView {border: 1px solid #aaaaaa} QListView::item {margin: 10px;}"

        self.setStyleSheet(f"background-color: {background}; color: {font}")

        label_template = QLabel("Choose a template:")
        combo_box = QComboBox()
        combo_box.insertItems(0, ["All Templates", "a", "b"])

        list_projects = QListWidget()
        list_projects.addItems(["Application (Qt)", "Application (Qt for Python)", "Library"])
        list_projects.setSelectionMode(QAbstractItemView.MultiSelection)
        list_projects.setStyleSheet(list_style)

        list_things = QListWidget()
        list_things.setStyleSheet(f"border: {border}; color: white;")
        icon = QIcon("./security-system.png")
        item = QListWidgetItem(icon, "Qt Widgets Application")
        list_things.addItem(item)

        label_description = QLabel("Description placeholder text goes in here")
        label_description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label_description.setStyleSheet("border: 1px solid #aaaaaa")

        layout_horizontala = QHBoxLayout()
        layout_horizontala.addWidget(label_template)
        layout_horizontala.addWidget(combo_box)

        layout_horizontalb = QHBoxLayout()
        layout_horizontalb.addWidget(list_projects)
        layout_horizontalb.addWidget(list_things)
        layout_horizontalb.addWidget(label_description)

        button_choose = QPushButton("Choose..")
        button_cancel = QPushButton("Cancel")
        button_cancel.clicked.connect(self.exit)

        layout_horizontalc = QHBoxLayout()
        layout_horizontalc.addStretch()
        layout_horizontalc.addWidget(button_choose)
        layout_horizontalc.addWidget(button_cancel)


        layout_vertical = QVBoxLayout()
        layout_vertical.addLayout(layout_horizontala)
        layout_vertical.addLayout(layout_horizontalb)
        layout_vertical.addLayout(layout_horizontalc)
        self.setLayout(layout_vertical)


        self.show()

    def exit(self):
        app.exit()

app = QApplication([])
window = MainWindow()
app.exec()
