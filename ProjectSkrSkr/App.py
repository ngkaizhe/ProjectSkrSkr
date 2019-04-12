import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QPlainTextEdit, QLabel, QFileDialog
from PyQt5 import QtGui
from UIManager import UIManager
import os

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

        #file location
        self.open_file_location = os.path.dirname(os.path.abspath(__file__))
        self.save_file_location = os.path.dirname(os.path.abspath(__file__))


        # set textbox
        self.setTextBox()

        # set button
        self.setButton()

        # set label
        self.setLabel()

        self.uiManager = UIManager()

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
        self.run_button.clicked.connect(self.run_result)

        self.set_button = QPushButton('set', self)
        self.set_button.move(350, 430)
        self.set_button.setFont(font)
        self.set_button.setStyleSheet("text-align: center")
        self.set_button.clicked.connect(self.set_up_ui_manager)

        self.clear_vector_button = QPushButton('clear vector', self)
        self.clear_vector_button.move(750, 430)
        self.clear_vector_button.setFont(font)
        self.clear_vector_button.setStyleSheet("text-align: center")
        self.clear_vector_button.clicked.connect(self.vector_clear)

        self.clear_matrix_button = QPushButton('clear matrix', self)
        self.clear_matrix_button.move(1050, 430)
        self.clear_matrix_button.setFont(font)
        self.clear_matrix_button.setStyleSheet("text-align: center")
        self.clear_matrix_button.clicked.connect(self.matrix_clear)

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

        self.vector_textbox = QPlainTextEdit(self)
        self.vector_textbox.move(600, 50)
        self.vector_textbox.resize(250, 350)
        self.vector_textbox.setReadOnly(True)

        self.matrix_textbox = QPlainTextEdit(self)
        self.matrix_textbox.move(900, 50)
        self.matrix_textbox.resize(250, 350)
        self.matrix_textbox.setReadOnly(True)

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

        self.vector_label = QLabel('Vector:', self)
        self.vector_label.setFont(font)
        self.vector_label.move(600, 25)

        self.matrix_label = QLabel('Matrix:', self)
        self.matrix_label.setFont(font)
        self.matrix_label.move(900, 25)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file",  self.open_file_location, "Text Files (*.txt)")
        tempPos = fileName.rfind('/')
        self.open_file_location = fileName[: tempPos + 1]

        if fileName:
            with open(fileName, 'r') as file:
                read_data = file.read()
            self.input_textbox.setPlainText(read_data)

    def saveFileDialog(self):
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", self.save_file_location,
                                                  "Text Files (*.txt)")
        tempPos = fileName.rfind('/')
        self.save_file_location = fileName[: tempPos + 1]

        if fileName:
            with open(fileName, 'w') as file:
                file.write(self.output_textbox.toPlainText())

            self.output_textbox.clear()

    def set_up_ui_manager(self):
        text = self.input_textbox.toPlainText()
        # misclick condition
        if text == '':
            return

        self.uiManager.set_arrais(text)
        self.input_textbox.clea r()
        self.update()

    def run_result(self):
        text = self.calculated_textbox.toPlainText()
        # misclick condition
        if text == '':
            return

        answer = self.output_textbox.toPlainText()
        answer += self.uiManager.run_result(text)
        self.output_textbox.setPlainText(answer)
        self.calculated_textbox.clear()
        self.update()

    def update(self):
        vector_string = ''
        k=0

        for i in self.uiManager.vector_arrais:
            vector_string += '$v' + str(k) + ':' + str(i) + '\n'
            k += 1

        self.vector_textbox.setPlainText(vector_string)

        matrix_string = ''
        k = 0

        for i in self.uiManager.matrix_arrais:
            matrix_string += '$m' + str(k) + ':' + str(i) + '\n'
            k += 1

        self.matrix_textbox.setPlainText(matrix_string)

    def vector_clear(self):
        if self.uiManager.vector_arrais and isinstance(self.uiManager.vector_arrais, list):
            self.uiManager.vector_arrais.clear()
            self.update()

    def matrix_clear(self):
        if self.uiManager.matrix_arrais and isinstance(self.uiManager.matrix_arrais, list):
            self.uiManager.matrix_arrais.clear()
            self.update()