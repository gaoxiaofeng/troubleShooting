# -*- coding: utf-8 -*-
from framework.modules.manager import ManagerFactory
import os,sys
from framework.modules.Import import Import
from framework.log.logger import logger
from framework.variable.variable import  *
from framework.output.Print import CONSOLE


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
        # self.logger.debug("%s be registered keyWord :%s"%(self.Manager.__class__.__name__,self.Manager.get_keyword()))

class KeywordBuilder(Builder):
    def __init__(self,folder):
        super(KeywordBuilder,self).__init__()
        self.import_dict = folder
        self.Manager =  ManagerFactory().getManager(LAYER.KeyWords)

class TestPointBuilder(Builder):
    def __init__(self,folder):
        super(TestPointBuilder,self).__init__()
        self.import_dict = folder
        self.Manager =  ManagerFactory().getManager(LAYER.TestPoint)

class CaseBuilder(Builder):
    def __init__(self,folder):
        super(CaseBuilder,self).__init__()
        self.import_dict = folder
        self.Manager = ManagerFactory().getManager(LAYER.Case)

class BuilderFactory(object):
    def __init__(self):
        super(BuilderFactory,self).__init__()
    def getBuilder(self,name):
        if name == LAYER.KeyWords:
            return KeywordBuilder(name)
        elif name ==  LAYER.TestPoint:
            return TestPointBuilder(name)
        elif name == LAYER.Case:
            return  CaseBuilder(name)
        else :
            return  None

