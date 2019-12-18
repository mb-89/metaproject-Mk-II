"""
Log feature

This is one of the features that should be included in all applications
and is different from application-specific features. It replaces the
logger placeholder of the rootapp with a proper logging object and 
adds the logging options tab to the "options" menu.
"""
import common
import sys
import logging
import os.path as op
from PyQt5 import QtCore,QtWidgets

class Log(common.Feature):
    enabled = True
    name = "log"

    @classmethod
    def integrateBackend(cls, app):
        log = logging.getLogger(app.appinfo["name"])
        path = app.cfg["workspace"]
        log.setLevel(logging.DEBUG)
        fh = logging.FileHandler(op.join(path,app.appinfo["name"]+".log"),mode="w")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s\t%(levelname)s\t%(message)s')
        log._fmt = formatter
        fh.setFormatter(formatter)
        log.addHandler(fh)
        log._STDerrLogger = StreamToLogger(log, logging.ERROR)
        log._origSTDerr = sys.stderr
        log._STDoutLogger = StreamToLogger(log, logging.INFO)
        log._origSTDout = sys.stdout
        sys.stdout = log._STDoutLogger
        app.log = log

        parent = common.NestedObj(app)

        infocmd = CMD_LogInfo(app) #lets expose the log cmds so we could use them via an external automation tool

        parent.addChild(infocmd)

        return parent

    @classmethod
    def integrateFrontend(cls, app): 
        """
        we build a logging window, add logging to the status bar and 
        add the logging options to the options menu
        """
        ui = app.frontend.ui
        parent = common.NestedObj(app)
        ui.logwindow = LogWidget(app.frontend,app)
        parent.logwindow = ui.logwindow
        parent.optwindow = LogOptions(app.frontend,app)

        toggleLog = common.GUIcmd("Tools/show log",parent.logwindow.togglehide,descr = "opens / hides the log window", shortcut = "Ctrl+L")
        toggleOpt = common.GUIcmd("Options/logging",parent.optwindow.togglehide,descr = "opens / hides the log window")

        parent.addChild(toggleLog)
        parent.addChild(toggleOpt)

        #add to statusbar:
        widget = ui.statusBar
        QtHandler = QtLog2StatusBarHandler()
        QtHandler.setFormatter(app.log._fmt)
        QtHandler.sig.connect(lambda x: widget.showMessage(x, 0))
        app.log.addHandler(QtHandler)

        #add to widget
        QtHandler = QtLog2TextEditHandler()
        QtHandler.setFormatter(app.log._fmt)
        QtHandler.sig.connect(parent.logwindow.widget().append)
        app.log.addHandler(QtHandler)
        app.log.debug("started logging into text widget")

        return parent

class LogWidget(QtWidgets.QDockWidget):
    def __init__(self, parent, app):
        super().__init__(parent)
        logging = QtWidgets.QTextEdit()
        logging.setReadOnly(True)
        logging.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        logging.customContextMenuRequested.connect(lambda x:self.LogContextMenu(logging, x))

        self.hide()
        self.setWidget(logging)
        #self.setFloating(True)
        parent.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self)
        self.resize(600,400)
        self.setWindowTitle(f'{app.appinfo["name"]} log')

    def togglehide(self):
        self.setVisible(self.isHidden())

    def LogContextMenu(self, widget, pos):
        menu = QtWidgets.QMenu()
        clearAction = QtWidgets.QAction("clear",widget)
        clearAction.triggered.connect(widget.clear)
        saveAction = QtWidgets.QAction("save to file",widget)
        saveAction.triggered.connect(lambda: self.savelog(widget))
        menu.addAction(clearAction)
        menu.addAction(saveAction)
        menu.exec(widget.viewport().mapToGlobal(pos))

    def savelog(self, widget):
        filename = QtWidgets.QFileDialog.getSaveFileName(None, "Save log to ...", "","*.*")
        if filename[0] != "": open(filename[0],"w").write(widget.toPlainText())

class LogOptions(QtWidgets.QDockWidget):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.hide()
        self.setFloating(True)
        self.setWindowTitle(f'{app.appinfo["name"]} log options')

    def togglehide(self):
        self.setVisible(self.isHidden())

class CMD_LogInfo(common.Backendcmd): 
    name = "log.info"
    description = "logs info message"
    args = [
        common.Backendarg("text", str, "string to print")
    ]
    def execute(self,argdict,retdict):
        self.rootapp.log.info(argdict["text"])
        yield 1.0

class StreamToLogger():
    """
    Fake file-like stream object that redirects writes to a logger instance.
    https://www.electricmonk.nl/log/2011/08/14/redirect-stdout-and-stderr-to-a-logger-in-python/
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):pass

class QtLog2StatusBarHandler(QtCore.QObject,logging.StreamHandler):
    sig = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def emit(self, logRecord):
        msg = self.format(logRecord)
        self.sig.emit(msg)

class QtLog2TextEditHandler(QtCore.QObject,logging.StreamHandler):
    sig = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()

    def emit(self, logRecord):
        msg = self.format(logRecord)
        self.sig.emit(msg)