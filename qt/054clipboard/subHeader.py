from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Button(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setProperty("class", "subheader_button")

class SubHeaderUi(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.initStyle()

    def initStyle(self):
        self.setProperty("class", "subheader")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.btn_widget.setContentsMargins(0, 0, 40, 0)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_layout.setSpacing(0)
        self.btn_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def initUi(self):
        self.layout = QHBoxLayout()
        self.btn_layout = QHBoxLayout()
        self.select_all_btn = QRadioButton()
        self.total_items = QPushButton("Total items: 0")
        self.total_items.setProperty("class", "subheader_total_items")
        self.favorite_btn = Button("Favourite")
        self.merge_btn = Button("Merge")
        self.export_btn = Button("Export")
        self.delete_btn = Button("Delete")
        self.length_lbl = QLabel("Length")
        self.btn_widget = QFrame()
        self.btn_layout.addWidget(self.favorite_btn)
        self.btn_layout.addWidget(self.merge_btn)
        self.btn_layout.addWidget(self.export_btn)
        self.btn_layout.addWidget(self.delete_btn)
        self.btn_widget.setLayout(self.btn_layout)

        self.layout.addWidget(self.select_all_btn)
        self.layout.addWidget(self.total_items)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_widget)
        self.layout.addWidget(self.length_lbl)

        self.setLayout(self.layout)

class SubHeader(SubHeaderUi):
    def __init__(self):
        super().__init__()

