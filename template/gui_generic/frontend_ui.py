# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'I:\006_projects\metaproject-Mk-II\template\gui_generic\frontend.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ui(object):
    def setupUi(self, ui):
        ui.setObjectName("ui")
        ui.resize(407, 279)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon_main"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ui.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(ui)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(self.centralWidget)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setObjectName("treeView")
        self.treeView.header().setVisible(False)
        self.verticalLayout.addWidget(self.treeView)
        ui.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(ui)
        self.statusBar.setObjectName("statusBar")
        ui.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(ui)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 407, 21))
        self.menuBar.setObjectName("menuBar")
        ui.setMenuBar(self.menuBar)

        self.retranslateUi(ui)
        QtCore.QMetaObject.connectSlotsByName(ui)

    def retranslateUi(self, ui):
        pass
import frontend_rc
