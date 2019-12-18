from fwk import base
import os.path as op

def main():
    app = base.App()
    app.prepare()
    app.start()

if __name__ == "__main__":main()