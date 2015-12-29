#!/usr/bin/python
# encoding=utf8 

import sys
import dataimport
import listfiles

reload(sys)
sys.setdefaultencoding('utf8')

# files stored here ...
path = '/home/hehj/workspace/worktasks_import/data/'

di = dataimport.dataimport()
# database server, changed here...
di.init(host='172.16.42.200',user='root',passwd='root')

# clear all data
# di.clearall()

files = listfiles.find_path(path)
total = len(files)
index = 1
done = 0
for f in files:
    print '[I][',index,'/',total,'] processing:',f
    n = di.import_file(f)
    if (n >= 0):
        done += 1
        print '[I]',n,'record(s) imported from ',f
    else:
        print '[E]',f
    index += 1

print '[I]all',total,'files processed,',done,'succeed'
di.uninit()

