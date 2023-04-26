"""
  pyside6-uic design.ui -o MainWindow.py
"""
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from clipping import Clipping
from subHeader import SubHeader
from fileHandler import FileHandler
from header import Header
#from header import Header

import time
import uuid
import sys

#QWidget
class Clipboard():
    def __init__(self, add_clipping):
        super().__init__()
        self.dont_add_next = False
        self.add_clipping = add_clipping
        self.clipboard = QGuiApplication.clipboard()
        self.clipboard.changed.connect(self.handle_changed)
        self.clipboard.dataChanged.connect(self.handle_data_changed)
        self.clipboard.findBufferChanged.connect(self.handle_find_buffer_changed)
        self.clipboard.selectionChanged.connect(self.handle_selection_changed)

    def handle_changed(self):
        pass

    " Gets called when user clicks copy/cut "
    " Types of mimeData: hasImage, hasHtml, hasText"
    def handle_data_changed(self):
        if self.dont_add_next:
            self.dont_add_next = False
            return
        mimeData = self.clipboard.mimeData()
        if mimeData.hasImage() == True:
            isImage = True
            now = str(round(time.time())) + ".png"
            image = mimeData.imageData()
            image.setText("path", now)
            self.add_clipping(image, isImage)
            if mimeData.imageData().save(f"./images/{now}") == False:
                print("Error saving image clipping")

        elif mimeData.hasText() == True:
            print("I have copied text adding to list...")
            isImage = False
            self.add_clipping(self.clipboard.text(), isImage)

        else :
            print("mimeData unkown")

    def handle_selection_changed(self):
        print("Selection changed")

    def handle_find_buffer_changed(self):
        print("Find buffer changed")

    def place_in_clipboard(self, data, isImage):
        self.dont_add_next = True
        if isImage:
            self.clipboard.setImage(data)
        else:
            self.clipboard.setText(data)

class MainWindowUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.initStyle()

    def initStyle(self):
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self.centralWidget().layout().setSpacing(0)

    def initUi(self):
        self.header = Header()
        self.subHeader = SubHeader()
        self.vlayout = QVBoxLayout()


        self.mainw = QWidget()
        self.vlayout = QVBoxLayout(self.mainw)
        self.scrollArea = QScrollArea(self.mainw)
        self.scrollArea.setWidgetResizable(True)
        #self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vlayout.addWidget(self.scrollArea)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setProperty("class", "scrollare")
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addStretch()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)


        self.vlayout.addWidget(self.header)
        self.vlayout.addWidget(self.subHeader)
        self.vlayout.addWidget(self.scrollArea)
        self.mainw.setLayout(self.vlayout)
        self.setCentralWidget(self.mainw)

        #self.vlayout.addWidget(self.clipping_container)
        self.widget = QWidget()

class MainWindow(MainWindowUi):
    def __init__(self):
        super().__init__()
        self.clipboard_disactivated = False
        self.clipboard = Clipboard(self.add_clipping)
        self.file = FileHandler()
        self.connect_subheader()
        self.connect_header()
        self.retrieve_saved_clippings()

    def connect_header(self):
        self.header.animatedToggle.clicked.connect(self.toggle_active)
        self.header.filter_view.view_all.clicked.connect(self.filter_all)
        self.header.filter_view.view_image.clicked.connect(self.filter_image)
        self.header.filter_view.view_fav.clicked.connect(self.filter_fav)

    def filter_all(self):
        print("filtering all")

    def filter_image(self):
        # removes clippings that don't contain images
        print(self.scrollAreaWidgetContents.children())

    def filter_fav(self):
        print("filtering fav")

    def connect_subheader(self):
        self.subHeader.select_all_btn.clicked.connect(self.select_all)
        self.subHeader.total_items.clicked.connect(self.select_all_radio)
        self.subHeader.delete_btn.clicked.connect(self.delete_selected)
        self.subHeader.favorite_btn.clicked.connect(self.favorite_selected)
        self.subHeader.merge_btn.clicked.connect(self.merge_selected)

    def retrieve_saved_clippings(self):
        for clipping in self.file.get_saved_clippings():
            clipping_text = clipping["text"]
            if clipping["isImage"] :
                image = QImage()
                path = clipping["text"]
                if image.load("./images/" + path) == False:
                    print(f"Unable to load {path} image")
                    continue
                image.setText("path", path) 
                self.add_clipping(image, clipping["isImage"], clipping["key"], clipping["created"], clipping["favorite"])
            else :
                self.add_clipping(clipping["text"], clipping["isImage"], clipping["key"], clipping["created"], clipping["favorite"])

    def add_clipping(self, clipping_text, isImage, key = 0, created = 0, favorite = 0):
        if self.clipboard_disactivated: return
        place_in_clipboard = self.clipboard.place_in_clipboard
        # will be 0 if new clipping 
        key = uuid.uuid4() if key == 0 else key
        now = time.time() if created == 0 else created
        favorite = False if favorite == 0 else favorite
        self.new_clipping = Clipping(place_in_clipboard, self.update_count, isImage, key, now, clipping_text, favorite)
        self.verticalLayout_2.insertWidget(0, self.new_clipping)
        self.update_count()

    def toggle_active(self):
        self.clipboard_disactivated = not self.clipboard_disactivated

    def select_all(self):
        if len(self.scrollAreaWidgetContents.children()) == 1:
            # Prevents activating toggle when there are no clippings
            self.subHeader.select_all_btn.setChecked(False)
        check_all = self.subHeader.select_all_btn.isChecked()
        for i, clipping in enumerate(self.scrollAreaWidgetContents.children()):
            if i == 0:
                continue
            clipping.handle_radio(check_all)

    def select_all_radio(self):
        checked = self.subHeader.select_all_btn.isChecked()
        self.subHeader.select_all_btn.setChecked(not checked)
        self.select_all()

    def delete_selected(self):
        deleted_count = 0
        # untoggles select all radio when deleting all
        self.subHeader.select_all_btn.setChecked(False)
        for i, clipping in enumerate(self.scrollAreaWidgetContents.children()):
            if i == 0:
                continue
            if clipping.am_i_selected(): deleted_count -= 1
            clipping.delete_if_selected()
        self.update_count(deleted_count)

    def update_count(self, clipping_count_change = 0):
        # if come from delete_selected deletions havent been carried out
        # so we pass through the deleted_count from delete selected
        current_count = len(self.scrollAreaWidgetContents.children()) - 1
        updated_count = current_count + clipping_count_change
        self.subHeader.total_items.setText("Total items: " + str(updated_count)) 

    def favorite_selected(self):
        for i, clipping in enumerate(self.scrollAreaWidgetContents.children()):
            if i == 0:
                continue
            clipping.toggle_favorite_if_selected()

    def closeEvent(self, event):
        # On close save state
        clipping_list = []
        for i, clipping in enumerate(self.scrollAreaWidgetContents.children()):
            if i == 0:
                continue
            text = clipping.clipping if not clipping.isImage else clipping.clipping.text('path')
            clipping_list.append({
                "key":str(clipping.key),
                "isImage": clipping.isImage,
                "created":clipping.created,
                "text":text,
                "favorite":clipping.am_favorite
                })

        self.file.save_clippings(clipping_list)

        
    def merge_selected(self):
        print("merging")
        # Loop over all 
        # disable merging for favorited

    def resizeEvent(self, e):
        pass

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    style = open("./style.qss").read()
    w.setStyleSheet(style)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

