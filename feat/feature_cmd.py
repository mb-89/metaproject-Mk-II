"""
cmd feature

Adds a commandline to the GUI that can be used to trigger all available backend commands
"""
import common
import re

from PyQt5 import QtWidgets,QtCore

class cmd(common.Feature):
    enabled = True
    name = "cmd"

    @classmethod
    def integrateBackend(cls, app):
        pass #we need no additional backend code

    @classmethod
    def integrateFrontend(cls, app): 
        """
        we add the commandline to the top of the window
        """
        ui = app.frontend.ui
        #add cmdline:
        cmdline = IntegratedCmd(app)

        return None

class IntegratedCmd(QtWidgets.QDockWidget):
    def __init__(self, app):
        super().__init__(app.frontend)
        self.rootapp = app
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

        toggleCmd = common.GUIcmd("Tools/show cmd",self.togglehide,descr = "opens / hides the console bar", shortcut = "Ctrl+^")

        app.frontend.addChild(toggleCmd)

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
        try:
            cmd,args = self.repattern.match(txt).groups()
            cmdobj = self.rootapp.backend.CMD[cmd]
        except:
            self.rootapp.log.error(f">>> {txt}: invalid cmd")
            return

        self.rootapp.log.info(f">>> {txt}")
        cmdobj.run(args,self.parseresult)


    def parseresult(self,res):
        if res["retcode"] != 0:
            self.rootapp.log.error(f">>> {res['err']}")