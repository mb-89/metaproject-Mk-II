from PyQt5 import QtCore, QtGui

class Backend(QtCore.QObject):
    def __init__(self, rootapp):
        super().__init__()
        self.rootapp = rootapp
        self.rootapp.backend = self
        self.DATA = Datastorage()
        self.rootapp.aboutToQuit.connect(self.close)

    def close(self):pass

class Datastorage(QtCore.QObject):
    def __init__(self):
        self.testTreeMdl = QtGui.QStandardItemModel()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(lambda:self.testTreeMdl.appendRow([QtGui.QStandardItem("bla")]))
        self.timer.start()