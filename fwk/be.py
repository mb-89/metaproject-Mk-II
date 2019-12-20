import common

class Backend(common.NestedObj):
    def __init__(self, rootapp):
        super().__init__(rootapp)
        self.rootapp = rootapp
        self.rootapp.backend = self
        self.CMD = {}

    def executeCmd(self,cmdDict):
        cmd     =cmdDict["cmd"]
        args    = cmdDict["args"]
        cb      = cmdDict["callback"]
        try:
            cmdobj = self.CMD[cmd]
        except:
            self.rootapp.log.info(f">>> {cmd}: unknown command")
            return
        cmdobj.run(args,cb)
        #