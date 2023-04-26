from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import json

import time

now = time.time()
print(now)


class FileHandler():
    def __init__(self):
        super().__init__()
        # Contains raw json
        self.file = open("clippings.json")
        self.raw = self.file.read()

        # Parses the raw string to JSON
        self.data = json.loads(self.raw)
        #for clipping in self.data:
        #    print(type(clipping["favorite"]))

    def get_saved_clippings(self):
        return self.data

    def save_clippings(self, clippings):
        with open('clippings.json', "w", encoding="utf-8") as f:
            json.dump(clippings, f, ensure_ascii=False, indent=4)
        #print(self.file)



        #data = "cunt"
        #self.writeData(data, len(data))
        #print(testData)


