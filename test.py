from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.acceptDrops()
        # set the title
        self.setWindowTitle("Image")
 
        # setting  the geometry of window
        self.setFixedSize(200,300)
 
        # creating label
        self.label = QLabel(self)
        self.label.setGeometry(20, 20, 160, 160) 
        self.label.setWindowFlags(Qt.FramelessWindowHint)
        self.label.setAttribute(Qt.WA_TranslucentBackground)

        # loading image
        self.pixmap = QPixmap('./image/joy.png')
        self.pixmap=self.pixmap.scaled(160, 160, QtCore.Qt.KeepAspectRatio)
        # adding image to label
        self.label.setPixmap(self.pixmap)
 
        # Optional, resize label to image size
        # self.label.resize(self.pixmap.width(),
        #                   self.pixmap.height())
 
        # show all the widgets
        self.show()
 
# create pyqt5 app
App = QApplication(sys.argv)
 
# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())