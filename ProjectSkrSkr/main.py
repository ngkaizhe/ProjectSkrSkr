from PyQt5.QtWidgets import *
from App import App
import sys

# main function

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App('Matrix Calculation', 600, 200, 630, 480)
    sys.exit(app.exec_())
