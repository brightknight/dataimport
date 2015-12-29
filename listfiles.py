# encoding=utf8 
import re
import os.path,sys

def find_path(path):
    files = []
    for f in os.listdir(path):
        src = os.path.join(path,f)
        if os.path.isdir(src):
            continue
        if (re.match('普利商用技术部周报_.*\.xls', f)):
            files.append(src)
    return files

