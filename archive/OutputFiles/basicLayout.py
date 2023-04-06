# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'basicLayout.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(785, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(40, 120, 631, 381))
        self.mainLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.board = QGridLayout()
        self.board.setObjectName(u"board")

        self.mainLayout.addLayout(self.board)

        self.info_commands = QVBoxLayout()
        self.info_commands.setObjectName(u"info_commands")
        self.info = QVBoxLayout()
        self.info.setObjectName(u"info")

        self.info_commands.addLayout(self.info)

        self.movement_layer_one = QHBoxLayout()
        self.movement_layer_one.setObjectName(u"movement_layer_one")
        self.move_up = QPushButton(self.horizontalLayoutWidget)
        self.move_up.setObjectName(u"move_up")

        self.movement_layer_one.addWidget(self.move_up)


        self.info_commands.addLayout(self.movement_layer_one)

        self.movement_layer_two = QHBoxLayout()
        self.movement_layer_two.setObjectName(u"movement_layer_two")
        self.move_left = QPushButton(self.horizontalLayoutWidget)
        self.move_left.setObjectName(u"move_left")

        self.movement_layer_two.addWidget(self.move_left)

        self.move_down = QPushButton(self.horizontalLayoutWidget)
        self.move_down.setObjectName(u"move_down")

        self.movement_layer_two.addWidget(self.move_down)

        self.move_right = QPushButton(self.horizontalLayoutWidget)
        self.move_right.setObjectName(u"move_right")

        self.movement_layer_two.addWidget(self.move_right)


        self.info_commands.addLayout(self.movement_layer_two)


        self.mainLayout.addLayout(self.info_commands)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 785, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.move_up.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.move_left.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.move_down.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.move_right.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
    # retranslateUi

