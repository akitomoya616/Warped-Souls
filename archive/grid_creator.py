from PySide6 import QtWidgets, QtGui, QtCore


class Window(QtWidgets.QWidget):
    def __init__(self, path):
        QtWidgets.QWidget.__init__(self)
        pixmap = QtGui.QPixmap("../images/Mountain.png")
        layout = QtWidgets.QGridLayout(self)
        for row in range(12):
            for column in range(12):
                label = QtWidgets.QLabel(self)
                pixmap = pixmap.scaled(50, 50, QtCore.Qt.KeepAspectRatio)
                label.setPixmap(pixmap)

                layout.addWidget(label, row, column)

        pixmap2 = QtGui.QPixmap("../images/Player.png")
        pixmap2 = pixmap2.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        label2 = QtWidgets.QLabel(self)
        label2.setPixmap(pixmap2)

        layout.addWidget(label2, 5, 7)
        #
        layout.removeWidget(label2)
        #
        layout.addWidget(label2, 8, 8)
        # print(layout.itemAtPosition(5, 7))
        # layout.removeWidget(layout.itemAtPosition(5, 7).widget())
        # widget1 = layout.itemAtPosition(3, 7).widget()
        # widget2 = layout.itemAtPosition(6, 12).widget()
        # layout.removeWidget(widget1)
        # layout.removeWidget(widget2)
        # widget1.hide()
        # widget2.close()
        # layout.addWidget(widget1, 6, 12)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window(sys.argv[1] if len(sys.argv) else '')
    window.setGeometry(500, 300, 100, 100)
    window.show()
    sys.exit(app.exec())
