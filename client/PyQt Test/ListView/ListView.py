from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import os
import requests
import json

class ListView(QWidget):
    def __init__(self, parent=None):
        super(ListView, self).__init__(parent)
        self.initUI()

    def get(self, point):
        response = requests.get(f"http://112.151.179.200:7474/taskmgr/import?dir={point}")
        data = json.loads(response.content.decode())
        self.listview.clear()
        for item in data:
            self.listview.addItem(json.dumps(item))

    def initAPI(self, point):
        self.cursor = point
        self.get(point)

    def goInto(self, filedir):
        js = json.loads(filedir[0].text())
        if js['stat'] == 'Folder':
            self.cursor = js['plain'].removeprefix("./import/resources/")
            self.get(self.cursor)
        
 
    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.listview = QListWidget()
        self.load = QPushButton('Load')
        self.into = QPushButton('Into')
        self.load.clicked.connect(lambda: self.initAPI('/'))
        self.into.clicked.connect(lambda: self.goInto(self.listview.selectedItems()))

        self.mainLayout.addWidget(self.listview)
        self.mainLayout.addWidget(self.load)
        self.mainLayout.addWidget(self.into)

        self.setLayout(self.mainLayout)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ListView()
    window.show()
    sys.exit(app.exec())