from PyQt5 import QtCore, QtWidgets, uic, QtGui
import os.path as op
import os
import subprocess
import importlib
import sys

def recompileAndLoadQtFiles(pyfilename):
    dirname = op.dirname(pyfilename)
    base = op.splitext(pyfilename)[0]

    uifilename = base+".ui"
    uiPYfilename = base+"_ui.py"
    qrcfilename = base+".qrc"
    qrcPYfilename = base+"_rc.py"

    if not op.isfile(uifilename): return None
    recompileUI = not op.isfile(uiPYfilename) or os.stat(uiPYfilename).st_mtime < os.stat(uifilename).st_mtime
    recompileQRC = op.isfile(qrcfilename) and (not op.isfile(qrcPYfilename) or os.stat(qrcPYfilename).st_mtime < os.stat(qrcfilename).st_mtime)

    if recompileQRC:    subprocess.call(["pyrcc5", qrcfilename, "-o", qrcPYfilename])
    if recompileUI:     subprocess.call(["pyuic5", uifilename, "--resource-suffix", "_rc", "-o", uiPYfilename])

    sys.path.append(dirname)
    mod = importlib.import_module(op.splitext(op.basename(uiPYfilename))[0])
    return mod.Ui_ui

class Frontend(QtWidgets.QMainWindow):
    def __init__(self, rootapp):
        super().__init__()
        self.rootapp = rootapp
        self.ui = recompileAndLoadQtFiles(op.abspath(__file__))()
        self.ui.setupUi(self)
        self.rootapp.frontend = self
        self.rootapp.aboutToQuit.connect(self.close)
        self.connect2backend()

    def connect2backend(self):
        self.ui.treeView.setModel(self.rootapp.backend.DATA.testTreeMdl)