from manager import TestPointManager,EngineManager,CaseManager
import os,sys
import pdb
import imp
from Import import Import


class Builder(object):
    def __init__(self):
        super(Builder,self).__init__()
        self.Import = Import()
    def list_python_file_by_path(self,path):
        file_list = os.listdir(path)
        pyFile_list = []
        for filename in file_list:
            if filename[-3:] == ".py" and  not filename.startswith("_"):
                pyFile_list.append(filename)

        return pyFile_list
class TestPointBuilder(Builder):
    def __init__(self):
        super(TestPointBuilder,self).__init__()
        self.import_dict = "testpoint"
    def builder(self):
        pyFile_list = self.list_python_file_by_path(self.import_dict)
        for pyFile in pyFile_list:
            packageName = "%s.%s"%(self.import_dict,pyFile[:-3])
            className = "%s"%pyFile[:-3]
            testObject = self.Import.importClass(packageName,className)
            TestPointManager.register(testObject)

class EngineBuilder(Builder):
    def __init__(self):
        super(EngineBuilder,self).__init__()
        self.import_dict = "engine"
    def builder(self):
        pyFile_list = self.list_python_file_by_path(self.import_dict)
        for pyFile in pyFile_list:
            packageName = "%s.%s"%(self.import_dict,pyFile[:-3])
            className = "%s"%pyFile[:-3]
            testObject = self.Import.importClass(packageName,className)
            EngineManager.register(testObject)

class CaseBuilder(Builder):
    def __init__(self):
        super(CaseBuilder,self).__init__()
        self.import_dict = "case"
    def builder(self):
        pyFile_list = self.list_python_file_by_path(self.import_dict)
        for pyFile in pyFile_list:
            packageName = "%s.%s"%(self.import_dict,pyFile[:-3])
            className = "%s"%pyFile[:-3]
            testObject = self.Import.importClass(packageName,className)
            CaseManager.register(testObject)



