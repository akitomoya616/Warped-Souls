from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys


class AddzyWindow(QMainWindow):
    def __init__(self):
        super(AddzyWindow, self).__init__()

        self.b1 = None
        self.b2 = None
        self.label = None
        self.msg = None

        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle('The First Window!')
        self.init_ui()

    def init_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText('Shark Tank!')
        self.label.move(100, 100)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText('Click It!')

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText('This is Button 2! This doesnt do anything')
        self.b2.move(200, 200)

        self.b1.clicked.connect(self.clicked)
        self.b1.clicked.connect(self.show_pop_up)

    def clicked(self):
        self.label.setText('Button was pressed!')
        self.update()

    def show_pop_up(self):
        self.msg = QMessageBox()
        self.msg.setText('Text Inside the Pop Up')
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.exec()

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = AddzyWindow()

    win.show()
    sys.exit(app.exec())


window()
