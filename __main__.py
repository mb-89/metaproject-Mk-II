from fwk import base
import os.path as op
import sys

def main():

    while(True):
        app = base.App()
        app.prepare()
        retcode = app.start()
        app.closeAllWindows()
        del app
        if retcode != base.CODE_RESTART:sys.exit(retcode)

if __name__ == "__main__":main()