from PyQt5 import QtCore, QtWidgets
import logging
import json

class NestedObj(QtCore.QObject):
    def __init__(self, parent):
        if parent is None:
            argv = [""]
            super().__init__(argv)
        else: super().__init__()
        
        self.parent = parent
        self.children = []
        if self.parent: self.parent.children.append(self)

    def start(self): 
        for x in self.children: x.start()

    def stop(self): 
        for x in self.children: x.stop()

    def prepare(self):
        for x in self.children: x.prepare()

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

    def findInChildren(self, targetclass, _container = list()):
        if isinstance(self, targetclass): _container.append(self)
        for x in self.children:
            x.findInChildren(targetclass, _container)
        return _container

class Feature(NestedObj):
    enabled = False
    name = "feature placeholder"
    @classmethod
    def isCompatibleWith(cls, app):
        if not cls.enabled: return False
        return True
    @classmethod
    def integrateBackend(cls, app): return None
    @classmethod
    def integrateFrontend(cls, app): return None

class LogPlaceholder(): #dont use this, replace it with a proper logger early
    def info(self, info, *args, **kwargs):print(f"INFO: {msg}")
    def warning(self, info, *args, **kwargs):print(f"WARNING: {msg}")
    def error(self, info, *args, **kwargs):print(f"ERROR: {msg}")
    def debug(self, info, *args, **kwargs):print(f"DEBUG: {msg}")

class GUIcmd(NestedObj):
    def __init__(self, path, fcn, descr = "", shortcut = None):
        super().__init__(0)
        self.path = path
        self.fcn = fcn
        self.descr = descr
        self.shortcut = shortcut

    def integrateInto(self, targetDict):
        action = QtWidgets.QAction()
        strippath = self.path.split("/")
        action.setText(strippath[-1])
        action.setToolTip(self.descr)
        if self.shortcut: action.setShortcut(self.shortcut)
        action.triggered.connect(self.fcn)

        for x in strippath[:-1]: targetDict = targetDict.setdefault(x,{})
        targetDict[strippath[-1]] = action

class Backendcmd(NestedObj):
    name = "basecmd"
    description = ""
    args = []
    rets = []

    def __init__(self, app): 
        super().__init__(0)
        self.rootapp = app

    def execute(self, argdict, retdict):
        for x in range(11):
            prog = x*0.1
            retdict["progress"] = prog
            yield prog
        retdict["retcode"] = 0

    def parseargs(self, args,cb):
        argsOk =    isinstance(args, dict)
        argsOk |=   isinstance(args, list)

        #try to parse as dict or json list
        if not argsOk:
            try:    
                args = json.loads(args)
                argsOk = True
            except: pass
        if not argsOk: #try to parse as list of args
            try:
                args = [x.strip() for x in args.split(",")]
                argsOk = True
            except: pass
        if not argsOk: args = {}

        #if the input is a list, make it a dict
        if isinstance(args, list):
            argdict = {}
            for arg,val in zip(self.args, args):
                try: val = arg.argtype(val)
                except: 
                    argsOk = False
                    break
                argdict[arg.name] = val
            args = argdict

        #if the input is a dict, check if it fits the required args
        for arg in self.args:
            name = arg.name
            try: args[name] = arg.eval(args[name])
            except: 
                if arg.default is not None: args[name] = arg.default
                else:
                    argsOk = False
                    break

        retdict = {}
        retdict["progress"] = 0 if argsOk else 1
        retdict["retcode"] = 0 if argsOk else -1
        retdict["err"] = "" if argsOk else "invalid args"

        QtCore.QTimer.singleShot(0,lambda: cb(retdict))
        return args, retdict, argsOk

    def run(self, args, cb):
        argdict, retdict, ok = self.parseargs(args,cb)
        if not ok: return
        
        for progress in self.execute(argdict,retdict):pass
        cb(retdict)

class Backendarg():
    def __init__(self, name, argtype, descr, default = None):
        self.name = name
        self.descr = descr
        self.argtype = argtype
        self.default = default

    def eval(self, input):
        return self.argtype(input)

    def __str__(self):
        return f"{self.name}\t{self.descr}\t{self.argtype}\tdefault: {self.default}"
