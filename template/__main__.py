import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from backend import backend
from gui_generic import frontend as fe_generic
import configparser
import os.path as op

def main():

    appinfo = configparser.ConfigParser()
    appinfo.read(op.join(op.dirname(__file__),"appinfo"))
    appinfo = dict(appinfo["info"])

    app = QApplication(sys.argv)
    app.info = appinfo
    app.setApplicationDisplayName(appinfo["name"])
    app.setWindowIcon(QtGui.QIcon(":/icon_main"))
    be = backend.Backend(app)

    fe = fe_generic.Frontend(app)
    fe.show()

    sys.exit(app.exec_())

if __name__ == "__main__":main()