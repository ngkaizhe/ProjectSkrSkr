import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QToolTip, QPlainTextEdit, QLabel, QFileDialog
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

        # set textbox
        self.setTextBox()

        # set button
        self.setButton()

        # set label
        self.setLabel()

        # self.openFileNamesDialog()
        # self.saveFileDialog()

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
        self.save_button.move(190, 430)
        self.save_button.setFont(font)
        self.save_button.setStyleSheet("text-align: center")
        self.save_button.clicked.connect(self.saveFileDialog)

        self.clear_button = QPushButton('clear', self)
        self.clear_button.move(30, 430)
        self.clear_button.setFont(font)
        self.clear_button.setStyleSheet("text-align: center")
        self.clear_button.clicked.connect(self.output_textbox.clear)

        self.open_button = QPushButton('open', self)
        self.open_button.move(460, 430)
        self.open_button.setFont(font)
        self.open_button.setStyleSheet("text-align: center")
        self.open_button.clicked.connect(self.openFileDialog)

        self.run_button = QPushButton('run', self)
        self.run_button.move(460, 200)
        self.run_button.setFont(font)
        self.run_button.setStyleSheet("text-align: center")

        self.set_button = QPushButton('set', self)
        self.set_button.move(350, 430)
        self.set_button.setFont(font)
        self.set_button.setStyleSheet("text-align: center")

    def setTextBox(self):
        # textbox part
        self.output_textbox = QPlainTextEdit(self)
        self.output_textbox.move(30, 50)
        self.output_textbox.resize(250, 350)

        self.input_textbox = QPlainTextEdit(self)
        self.input_textbox.move(350, 250)
        self.input_textbox.resize(200, 150)

        self.calculated_textbox = QPlainTextEdit(self)
        self.calculated_textbox.move(350, 50)
        self.calculated_textbox.resize(200, 130)

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

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file", "C://", "Text Files (*.txt)")

        if fileName:
            with open(fileName, 'r') as file:
                read_data = file.read()

            self.input_textbox.setPlainText(read_data)

    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", "C://",
                                                  "Text Files (*.txt)")
        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.output_textbox.toPlainText())
