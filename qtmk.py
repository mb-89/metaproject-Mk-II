from glob import glob
import os.path as op
from lxml import etree
import subprocess

for ui in glob(op.join(op.dirname(__file__),"**","*.ui"),recursive=True):

    content = etree.parse(ui).getroot()
    res = content.find("resources")
    if res is not None:
        dirname = op.dirname(ui)
        qrcs = []
        for file in [x.attrib.get("location") for x in res.findall("include")]:
            if file.endswith(".qrc"): qrcs.append(op.join(dirname, file))
        
        for qrc in qrcs: subprocess.call(["pyrcc5", qrc, "-o", qrc.replace(".qrc", "RC.py")])

    subprocess.call(["pyuic5", ui, "--resource-suffix", "RC", "-o", ui.replace(".ui", "_ui.py")])