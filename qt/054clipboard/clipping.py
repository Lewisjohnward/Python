from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

import time 

class SelectRadio(QRadioButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

class Generic_Label(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

class TimeBubble(Generic_Label):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(110, 40))
        self.setProperty("class", "clipping_time_bbl")

class Text(Generic_Label):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "clipping_text")
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setWordWrap(True)
        self.setMaximumWidth(500)

class Image(Generic_Label):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMaximumWidth(500)

class Generic_btn(QPushButton):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

class Star_btn(Generic_btn):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "star_btn")
        self.setIcon(QIcon("./icons/star.png"))

class Copy_btn(Generic_btn):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "eye_btn, eye")
        self.setIcon(QIcon("./icons/copy.png"))

class Send_btn(Generic_btn):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "send_btn")
        self.setIcon(QIcon("./icons/send.png"))

class Upload_btn(Generic_btn):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "upload_btn")
        self.setIcon(QIcon("./icons/upload.png"))

class Delete_btn(Generic_btn):
    def __init__(self):
        super().__init__()
        self.setProperty("class", "delete_btn")
        self.setIcon(QIcon("./icons/delete.png"))

class Length(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignRight| Qt.AlignVCenter)
        self.setFixedSize(QSize(40, 40))

class ClippingUi(QFrame):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.initStyle()

    def initStyle(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setProperty("class", "clipping_container")


    def initUi(self):
        self.time_bbl = TimeBubble()
        self.radio_btn = SelectRadio()
        self.clipping_text = Text()
        self.image = Image()
        self.star_btn = Star_btn()
        self.copy_btn = Copy_btn()
        self.send_btn = Send_btn()
        self.upload_btn = Upload_btn()
        self.delete_btn = Delete_btn()
        self.length = Length()

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.star_btn)
        self.btn_layout.addWidget(self.copy_btn)
        self.btn_layout.addWidget(self.send_btn)
        self.btn_layout.addWidget(self.upload_btn)
        self.btn_layout.addWidget(self.delete_btn)
        self.btn_layout.setSpacing(0)
        self.btn_layout.setContentsMargins(0, 0, 0, 0)
        self.btn_layout_container = QFrame()
        self.btn_layout_container.setLayout(self.btn_layout)
        self.btn_layout_container.setContentsMargins(0, 0, 0, 0)
        self.btn_layout_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_layout_container.setProperty("class", "clipping_btn_container")


        self.layout = QHBoxLayout()
        self.layout.addWidget(self.radio_btn)
        self.layout.addWidget(self.time_bbl)
        self.layout.addWidget(self.clipping_text)
        self.layout.addWidget(self.image)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_layout_container)
        self.layout.addWidget(self.length)
        self.setLayout(self.layout)

class Clipping(ClippingUi):
    def __init__(self, place_in_clipboard, update_count, isImage, key, created, text, favorite):
        super().__init__()
        self.place_in_clipboard = place_in_clipboard
        self.update_count = update_count
        self.key = key
        self.created = created
        self.isImage = isImage
        self.selected = False
        self.clipping = text
        self.am_favorite = favorite
        self.init_clipping()


    def init_clipping(self):
        # Radio select button
        self.radio_btn.clicked.connect(self.toggle_radio)
        # Get current date/time
        #self.now = datetime.now()
        # Clipping text
        if self.isImage:
            self.image.setPixmap(QPixmap(self.clipping))
        else: 
            self.clipping_text.setText(self.clipping)
            # Clipping length
            self.length.setText(str(len(self.clipping)))
        # Delete button
        self.delete_btn.clicked.connect(self.delete_me)
        # star/favorite button
        self.star_btn.clicked.connect(self.favorite)
        # Time clipping was taken
        self.update_time_since_creation()
        # Setup favorite styling if favorite
        self.change_favorite_style()
        # Onclick copy to clipboard
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

    def copy_to_clipboard(self):
        self.place_in_clipboard(self.clipping, self.isImage)

    def update_time_since_creation(self):
        now = time.time()
        time_elapsed = round((now - self.created) / 60)
        if time_elapsed < 1:
            time_elapsed = "A few secs ago"
        elif time_elapsed < 60:
            time_elapsed = f"{time_elapsed} mins ago"
        elif time_elapsed < (60 * 24):
            hours_elapsed = round(time_elapsed / 60)
            time_elapsed = f"{hours_elapsed} hours ago"
        else:
            days_elapsed = round(time_elapsed / (60 * 24))
            time_elapsed = f"{days_elapsed} days ago"

        time_since = time_elapsed
        self.time_bbl.setText(time_since)

    def toggle_radio(self):
        self.selected = not self.selected
        self.radio_btn.setChecked(self.selected)

    def handle_radio(self, value):
        self.selected = value
        self.radio_btn.setChecked(value)

    def delete_me(self):
        self.deleteLater()
        self.update_count(-1)

    def am_i_selected(self):
        if not self.am_favorite: 
            return self.selected

    def favorite(self):
        self.am_favorite = not self.am_favorite
        self.change_favorite_style()

    def delete_if_selected(self):
        if self.selected == True and not self.am_favorite: 
            self.delete_me()

    def toggle_favorite_if_selected(self):
        if self.selected == True: 
            self.am_favorite = True
        self.change_favorite_style()

    def change_favorite_style(self):
        if self.am_favorite:
            self.star_btn.setStyleSheet("background: gold")
            self.delete_btn.setEnabled(False)
        else:
            self.star_btn.setStyleSheet("")
            self.delete_btn.setEnabled(True)

    def mousePressEvent(self, e):
        self.toggle_radio()


