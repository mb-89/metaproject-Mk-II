import os.path as op
import os
import shutil
import tempfile
import time
import stat
import sys
import json

#make a copy of the current project:
dir = op.dirname(__file__)
dst = op.join(dir,"dist")

name = sys.argv[1]
descr = sys.argv[2]

shutil.rmtree(dst, ignore_errors=True)
os.remove(name+".py")

with tempfile.TemporaryDirectory() as tmpdst:
    tmp = op.join(tmpdst,"tmp")
    shutil.copytree(dir, tmp)
    os.system('rmdir /S /Q "{}"'.format(op.abspath(op.join(tmp,".git")))) #bc .git is stubborn...
    shutil.rmtree(op.join(tmp,".vscode"), ignore_errors=True)
    shutil.rmtree(op.join(tmp,"workspace"), ignore_errors=True)
    shutil.rmtree(op.join(tmp,"fwk","__pycache__"), ignore_errors=True)
    shutil.rmtree(op.join(tmp,"__pycache__"), ignore_errors=True)
    shutil.rmtree(op.join(tmp,"feat","__pycache__"), ignore_errors=True)

    appinfo = json.loads(open(op.join(tmp,"fwk","appinfo.json"),"r").read())
    appinfo["name"]= name
    appinfo["description"]= descr
    json.dump(appinfo,open(op.join(tmp,"fwk","appinfo.json"),"w"),sort_keys=True,indent=4, separators=(',', ': '))

    shutil.move(tmp,dst)
    shutil.make_archive(name, 'zip', dst)
    shutil.rmtree(dst, ignore_errors=True)
    os.rename(name+".zip",name+".py")
