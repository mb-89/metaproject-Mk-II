from .be import Backend
from .fe import Frontend
from fwk import common

from PyQt5.QtWidgets import QApplication

import os.path as op
import json
import argparse
import sys
import importlib
import pkg_resources
import os

CODE_RESTART = -1337

class App(QApplication, common.NestedObj):
    def __init__(self):
        super().__init__(None)

        self.appinfo = json.loads(pkg_resources.resource_string(__name__, "appinfo.json"))

        parser = argparse.ArgumentParser(description=self.appinfo["description"])
        parser.add_argument("--workspace", type=str, help = "folder to work in.", default = None)
        parser.add_argument("--features", type=str, help = "folder from which to import features.", default = None)
        self.cfg = vars(parser.parse_args())


        if self.cfg["workspace"]: workspacepath = op.abspath(self.cfg["workspace"])
        else: workspacepath = op.abspath(op.join(os.getcwd(),"workspace"))

        os.makedirs(workspacepath,exist_ok=True)
        
        cfgpath = op.join(workspacepath,"cfg.json")
        addcfg = json.loads(open(cfgpath,"r").read()) if op.isfile(cfgpath) else {}
        for k,v in addcfg: self.cfg[k] = v
        self.cfg["workspace"] = workspacepath

        featurepath   = pkg_resources.resource_filename(__name__, "/../feat") if self.cfg["features"] is None else op.abspath(self.cfg["features"])
        self.cfg["features"] = featurepath

        self.backend  = Backend(self)
        self.frontend = Frontend(self)
        self.log = common.LogPlaceholder()
        self.integrateFeatures()

    def buildFeatureFileDict(self, featdir):
        try: fDict = json.loads(open(op.join(featdir,"features.json"),"r").read())
        except: return {}
        poplist = []
        for k in fDict:
            if k.startswith("_"):
                poplist.append(k)
                continue
            fDict[k] = op.abspath(op.join(featdir,fDict[k]))
        for k in poplist: fDict.pop(k)
        return fDict

    def integrateFeatures(self):
        feats = []
        featurefiles = self.buildFeatureFileDict(self.cfg["features"])
        for name, file in featurefiles.items():

            modname = op.splitext(op.basename(file))[0]
            dirname = op.dirname(file)
            sys.path.append(dirname)
            mod = importlib.import_module(modname)
            for name in dir(mod):
                x = getattr(mod,name)
                try: 
                    if issubclass(x, common.Feature): feats.append(x)
                except: continue

        self.FEAT = {}
        for fc in feats:
            if not fc.isCompatibleWith(self):return
            self.FEAT[fc.name] = fc(self)
        
        guicmds = []
        backendcmds = []
        dataelems = []
        self.findInChildren(common.GUIcmd,guicmds)
        self.findInChildren(common.Backendcmd,backendcmds)
        self.findInChildren(common.BackendData,dataelems)

        self.frontend.buildMenues(guicmds)
        self.CMD = dict([(x.name, x) for x in backendcmds])
        self.DATA = dict([(x.name, x) for x in dataelems])

    def prepare(self):
        self.setApplicationDisplayName(self.appinfo["name"])
        super().prepare()

    def start(self):
        super().start()
        return self.exec_()