from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.template._BaseTestPoint import _BaseTestPoint
@singleton
class Nbi3gcERRORLogParse(_BaseTestPoint):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.level = LEVEL.NOCRITICAL

    def _checkpoint(self):
        parsedLogClassContent,parsedLogClassCount = self.getLogParsedResult("/var/opt/oss/log/nbi3gc","ERROR")
        for key in parsedLogClassCount:
            print "class:< %s > raise Error %s times, and content as below:"%(key,parsedLogClassCount[key])
            if parsedLogClassContent.has_key(key):
                print "\n".join(parsedLogClassContent[key])
            else:
                print "NA"
        if parsedLogClassCount == {}:
            self.status = STATUS.PASS
        else:
            self.status = STATUS.FAIL
