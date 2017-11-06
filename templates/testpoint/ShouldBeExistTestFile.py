from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template.TestPoint import *
@singleton
class ShouldBeExistTestFile(TestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()

    def _checkpoint(self):
        testFilePath = "/home/testfile"
        exist = self.is_exist_file(testFilePath)
        if exist:
            self.status = STATUS.PASS
            print "%s is exist."%testFilePath
        else:
            self.status = STATUS.FAIL
            print "File %s is not exist."%testFilePath
            self.IMPACT.append("the %s is not exist."%testFilePath)
            self.RCA.append("the %s is not exist."%testFilePath)
            self.FIXSTEP.append("touch a File:%s"%testFilePath)
            self.AUTOFIEXSTEP.append("touchFile(%s)"%testFilePath)



