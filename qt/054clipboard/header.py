from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from animatedToggle import AnimatedToggle


class SearchBar(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setProperty("class", "header_searchbar")

        self.line_edit = QLineEdit()
        self.line_edit.setProperty("class", "header_searchbar_line_edit")
        self.line_edit.setPlaceholderText("search")
        self.searchIco = QPushButton()
        self.searchIco.setIcon(QIcon("./icons/search.png"))
        self.searchIco.setProperty("class", "header_searchbar_search_icon")
        self.setProperty("class", "header_searchbar")
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.searchIco)


class Btn(QPushButton):
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setProperty("class", "header_filter_button")
        self.setMinimumWidth(100)

class FilterView(QFrame):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setProperty("class", "header_filter_view")
        self.view_all = Btn("All")
        self.view_text = Btn("Text")
        self.view_image = Btn("Image")
        self.view_fav = Btn("Fav")
        self.layout.addWidget(self.view_all)
        self.layout.addWidget(self.view_fav)
        self.layout.addWidget(self.view_image)
        self.layout.addWidget(self.view_text)


class HeaderUi(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.initStyle()

    def initStyle(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setProperty("class", "header")
        self.animatedToggle.setProperty("class", "header_toggle")

    def initUi(self):
        self.layout = QHBoxLayout(self)
        self.animatedToggle = AnimatedToggle(None, Qt.gray, "#269e52", Qt.white, "#44999999", "#66d18e")
        self.animatedToggle.setMinimumWidth(60)
        self.animatedToggle.setMaximumHeight(30)
        self.animatedToggle.setChecked(True)
        self.animatedToggle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.filter_view = FilterView()
        self.search_bar = SearchBar()
        self.layout.addWidget(self.animatedToggle)

        self.layout.addStretch()
        self.layout.addWidget(self.filter_view)
        self.layout.addStretch()
        self.layout.addWidget(self.search_bar)


class Header(HeaderUi):
    def __init__(self):
        super().__init__()
