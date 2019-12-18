"""
help feature

adds a backend cmd that prints all backend cmd helps
"""
import common

from PyQt5 import QtWidgets

class help(common.Feature):
    enabled = True
    name = "help"

    @classmethod
    def integrateBackend(cls, app):
        parent = common.NestedObj(app)
        parent.addChild(CMD_help(app))

class CMD_help(common.Backendcmd):
    name = "help"
    description = "prints help for backend cmds"

    args = [
        common.Backendarg("cmd", str, "prints help for selected cmd", default = ""),
        common.Backendarg("rettype", int, "0 for string, 1 for json", default = 0),
        common.Backendarg("log", bool, "true to log result", default = True)
    ]

    def execute(self, argdict, retdict):

        if argdict["cmd"] == "" and argdict["rettype"] == 0: #case 0: create text for all cmds
            lines = [self.rootapp.appinfo['name']+" help\n\navailable backend commands / help(<cmd>) for details"]
            for x in sorted(self.rootapp.backend.CMD.keys()):
                cmd = self.rootapp.backend.CMD[x]
                lines.append(f"{x}\t{cmd.description}\t{len(cmd.args)} args\t{len(cmd.rets)} rets")
            lines.append("\n")
            txt = "\n".join(lines)
        
        if argdict["cmd"] != "" and argdict["rettype"] == 0: #case 1: create text for specific cmd
            target = self.rootapp.backend.CMD.get(argdict["cmd"] )
            if target is None: 
                retdict["retcode"] = -2
                retdict["err"] = f"cmd {argdict['cmd']} not available"
                return 1.0
            lines = [f"help for cmd <{target.name}>\n\n{target.name}: {target.description}\n\nInputs"]
            if not target.args:lines.append("--")
            for arg in target.args:lines.append(f"{str(arg)}")
            lines.append("\nReturns")
            if not target.rets:lines.append("--")
            for ret in target.rets:lines.append(f"{str(ret)}")
            lines.append("\n")
            txt = "\n".join(lines)


            #lines = [self.rootapp.appinfo['name']+" help:\n\navailable backend commands / help(<cmd>) for details:"]
            #for x in sorted(self.rootapp.backend.CMD.keys()):
            #    cmd = self.rootapp.backend.CMD[x]
            #    lines.append(f"{x}\t{cmd.description}\t{len(cmd.args)} args\t{len(cmd.rets)} rets")
            #txt = "\n".join(lines)


        if argdict["log"]:
            self.rootapp.log.info(txt)

        yield 1.0
