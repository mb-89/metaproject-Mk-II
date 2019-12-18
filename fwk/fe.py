import common
from . import fe_ui
from PyQt5 import QtWidgets

class Frontend(QtWidgets.QMainWindow, common.NestedObj):
    def __init__(self, rootapp):
        super().__init__(rootapp)
        self.rootapp = rootapp
        self.rootapp.frontend = self
        self.ui = fe_ui.Ui_ui()
        self.ui.setupUi(self)

    def start(self):
        super().start()
        self.show()

    def buildMenues(self, menucmds):

        menudict = {}
        for x in menucmds: x.integrateInto(menudict)
        for k in sorted(menudict.keys()): 
            newmenu = self._buildMenu(self.ui.menuBar,k,menudict[k])
            self.ui.menuBar.addAction(newmenu.menuAction())
    
    def _buildMenu(self, parent, name, entries):
        if isinstance(entries,dict):
            newmenu = QtWidgets.QMenu(parent)
            newmenu.setObjectName(name)
            newmenu.setTitle(name)
            for k in sorted(entries.keys()): self._buildMenu(newmenu,k,entries[k])
            return newmenu
        parent.addAction(entries)
        entries.setParent(parent)