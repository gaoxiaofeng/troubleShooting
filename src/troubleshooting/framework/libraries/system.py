import sys,os
import shutil
def createDir(path):
    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except Exception,e:
            raise IOError(e)
def clean(path=os.getcwd()):
    for file in os.listdir(path):
        absolute_path = os.path.join(path, file)
        if os.path.isdir(absolute_path):
            if len(file) == 7 and file.endswith(".d"):

                try:
                    shutil.rmtree(absolute_path)
                except Exception,e:
                    print "failed to remove %s"%absolute_path
