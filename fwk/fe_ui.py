# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\template\fwk\fe.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ui(object):
    def setupUi(self, ui):
        ui.setObjectName("ui")
        ui.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(ui)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.centralLayout = QtWidgets.QVBoxLayout()
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName("centralLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.centralLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.centralLayout)
        ui.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(ui)
        self.statusBar.setObjectName("statusBar")
        ui.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(ui)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menuBar.setObjectName("menuBar")
        ui.setMenuBar(self.menuBar)

        self.retranslateUi(ui)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui):
        pass