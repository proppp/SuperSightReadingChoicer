# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import sys
import os, random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication



class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("SightReadingChoicer")
        self.initUI()

    def clicked(self):
        self.label.setText("clickss")
        self.update()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my first label")
        self.label.move(50, 50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("CHILL")
        self.b1.move(100, 110)
        self.b1.clicked.connect(self.clicked)
        self.b1.clicked.connect(clickingthebutton)

    def update(self):
        self.label.adjustSize()


def clickingthebutton():
    print("clicked")

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(100, 100, 500, 500)
        self.setWindowTitle("coococ")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("my first label")
        self.label.move(50, 50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("CHILL")
        self.b1.move(100, 110)
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText(f"Your file is: {get_random_files2(extension)}")
        self.update()

    def update(self):
        self.label.adjustSize()


def clickingthebutton():
    print("clicked")


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
