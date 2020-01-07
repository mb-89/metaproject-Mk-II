"""
cmd feature

Adds a commandline to the GUI that can be used to trigger all available backend commands
"""
from fwk import common
import re

from PyQt5 import QtWidgets,QtCore

class cmd(common.Feature):
    enabled = True
    name = "cmd"

    def __init__(self, app):
        super().__init__(app) #app is now our parent
        self.rootapp = app
        self.backend = common.FeatureBackend(self)
        self.frontend = CmdFrontend(self)

        #these are the public commands/data of this feature
        app.frontend.addChild(common.GUIcmd("Tools/show cmd",self.frontend.widget.togglehide,descr = "opens / hides the console bar", shortcut = "Ctrl+^"))

class CmdFrontend(common.FeatureFrontend):
    def __init__(self, rootfeature):
        super().__init__(rootfeature) #frontend is now our parent
        self.widget = CmdWidget(self)

class CmdWidget(QtWidgets.QDockWidget):
    executeCmd = QtCore.pyqtSignal(dict)
    def __init__(self, parent):
        super().__init__()
        self.rootapp = parent.rootapp
        app = parent.rootapp
        self.txt = QtWidgets.QLineEdit(self)
        empty = QtWidgets.QWidget(self)
        self.setTitleBarWidget(empty)
        self.setWindowTitle("cmd")
        self.setWidget(self.txt)
        self.txt.returnPressed.connect(self.parse)
        app.frontend.addDockWidget(QtCore.Qt.TopDockWidgetArea, self)
        self.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(QtCore.Qt.TopDockWidgetArea)
        self.setVisible(False)
        self.repattern = re.compile(r"(.*)\((.*)\)")
        self.executeCmd.connect(self.rootapp.backend.executeCmd)

    def togglehide(self):
        self.setVisible(not self.isVisible())
        if self.isVisible():
            self.txt.setFocus()

    def parse(self):
        txt = self.txt.text()
        self.txt.clear()
        if not txt.endswith(")"):txt+="()"
        try:self.rootapp.frontend.ui.logwindow.setHidden(False)
        except:pass

        try: cmd,args = self.repattern.match(txt).groups()
        except: 
            self.rootapp.log.error(f">>> {txt}: syntax error")
            return
        #    
        #    cmdobj = self.rootapp.backend.CMD[cmd]
        #except:
        #    
        #    return

        #self.rootapp.log.info(f">>> {txt}")
        cmdDict = {
            "args": args,
            "cmd": cmd,
            "callback":self.parseresult
        }
        self.executeCmd.emit(cmdDict)

    def parseresult(self,res):
        if res["retcode"] != 0:
            self.rootapp.log.error(f">>> {res['err']}")