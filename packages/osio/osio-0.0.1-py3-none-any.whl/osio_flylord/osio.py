import shutil
import os
from os.path import exists

def cp(src, dst):
    shutil.copyfile(src, dst)
    return

def rm(src):
    if (exists(src)):
        os.remove(src)

def rn(src, dst):
    if(exists(dst)):
        raise RuntimeError("file already exists: " + dst)
    if(exists(src)):
        os.rename(src,dst)

def mkdir(nm):
    import os.path as path
    if (path.exists(nm)):
        return
    os.mkdir(nm)

def rmdir(nm):
    import os.path as path
    import os as os
    if (path.exists(nm)):
        os.removedirs(nm)
        return

#cp("testfile1.txt", "1.txt")
#rn("1.txt", "t1.txt")

