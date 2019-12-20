from .be import Backend
from .fe import Frontend
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication
import os.path as op
import json
import argparse
import common
import sys
import importlib
import pkg_resources
import os

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
        for k in fDict:
            fDict[k] = op.abspath(op.join(featdir,fDict[k]))
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

        self.features = {}
        for fc in feats:
            if not fc.isCompatibleWith(self):return
            be = fc.integrateBackend(self)
            fe = fc.integrateFrontend(self)
            if be is None and fe is None: continue
            self.features[fc.name] = {"backend":be,"frontend":fe}
        
        guicmds = []
        backendcmds = []
        self.findInChildren(common.GUIcmd,guicmds)
        self.findInChildren(common.Backendcmd,backendcmds)
        self.frontend.buildMenues(guicmds)
        self.backend.CMD = dict([(x.name, x) for x in backendcmds])

    def prepare(self):
        self.setApplicationDisplayName(self.appinfo["name"])
        super().prepare()

    def start(self):
        super().start()
        sys.exit(self.exec_())