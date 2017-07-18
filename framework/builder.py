from framework.manager import KeywordManagerInstance,TestPointManagerInstance,CaseManagerInstance
import os,sys
from framework.Import import Import
from framework.log.logger import logger


class Builder(object):
    def __init__(self):
        super(Builder,self).__init__()
        self.Import = Import()
        self.logger = logger()
        self.Manager = None
        self.import_dict = None
    def list_python_file_by_path(self,path):
        file_list = os.listdir(path)
        pyFile_list = []
        for filename in file_list:
            if filename[-3:] == ".py" and  not filename.startswith("_"):
                pyFile_list.append(filename)
        return pyFile_list
    def builder(self):
        if self.import_dict == None :
            raise Exception("Builder Attribute import_dict is None.")
        if self.Manager == None:
            raise  Exception("Builder Attribute Manager is None.")
        pyFile_list = self.list_python_file_by_path(self.import_dict)
        for pyFile in pyFile_list:
            packageName = "%s.%s"%(self.import_dict,pyFile[:-3])
            className = "%s"%pyFile[:-3]
            Object = self.Import.importClass(packageName,className)
            self.Manager.register(Object)
        self.logger.debug("%s be registered keyWord :%s"%(self.Manager.__class__.__name__,self.Manager.get_keyword()))


class TestPointBuilder(Builder):
    def __init__(self):
        super(TestPointBuilder,self).__init__()
        self.import_dict = "testpoint"
        self.Manager =  TestPointManagerInstance

class KeywordBuilder(Builder):
    def __init__(self):
        super(KeywordBuilder,self).__init__()
        self.import_dict = "testlibrary"
        self.Manager =  KeywordManagerInstance
class CaseBuilder(Builder):
    def __init__(self):
        super(CaseBuilder,self).__init__()
        self.import_dict = "testcase"
        self.Manager = CaseManagerInstance

class BuilderFactory(object):
    def __init__(self):
        super(BuilderFactory,self).__init__()
    def getBuilder(self,name):
        if name == "keyword":
            return KeywordBuilder()
        elif name == "testpoint":
            return TestPointBuilder()
        elif name == "case":
            return  CaseBuilder()
        else :
            return  None

