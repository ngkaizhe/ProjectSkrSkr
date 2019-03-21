import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QToolTip, QPlainTextEdit, QLabel
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon

class App(QWidget):
 
    # constructor
    def __init__(self, title, left, top, width, height):
        super().__init__()

        self.title = title
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        
        #set button
        self.setButton()

        #set textbox
        self.setTextBox()

        #set label
        self.setLabel()

        self.initUI()
 
    # init UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    # set button
    def setButton(self):
        #font
        font = QtGui.QFont()
        font.setPointSize(10)
        

        # button part
        self.save_button = QPushButton('save', self)       
        self.save_button.move(180, 430)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet("text-align: center")
        

        self.open_button = QPushButton('open', self)
        self.open_button.move(450, 430)
        self.open_button.setFont(font)
        self.open_button.setStyleSheet("text-align: center")

    #set textbox
    def setTextBox(self):
        # textbox part
        self.output_textbox = QPlainTextEdit(self)
        self.output_textbox.move(30, 50)
        self.output_textbox.resize(250,350)

        self.input_textbox = QPlainTextEdit(self)
        self.input_textbox.move(350, 250)
        self.input_textbox.resize(200,150)

        self.calculated_textbox = QPlainTextEdit(self)
        self.calculated_textbox.move(350, 50)
        self.calculated_textbox.resize(200,130)

    #set label
    def setLabel(self):
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(100)

        self.output_label = QLabel('Output:', self)
        self.output_label.setFont(font)
        self.output_label.move(30, 25)

        self.calculated_label = QLabel('Calculation:', self)
        self.calculated_label.setFont(font)
        self.calculated_label.move(350, 25)

        self.input_label = QLabel('Input:', self)
        self.input_label.setFont(font)
        self.input_label.move(350, 225)