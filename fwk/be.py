import common

class Backend(common.NestedObj):
    def __init__(self, rootapp):
        super().__init__(rootapp)
        self.rootapp = rootapp
        self.rootapp.backend = self