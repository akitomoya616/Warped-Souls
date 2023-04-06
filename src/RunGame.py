from PySide6 import QtWidgets, QtGui, QtCore
import sys

from Board import Board
from UI import UI


def main():
    # Application Initialization
    app = QtWidgets.QApplication(sys.argv)

    # Create the Board
    game = UI()
    game.show()

    # Exit the application on close
    sys.exit(app.exec())


main()
