# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.manager import ManagerFactory
from os.path import dirname,abspath,join
from os import listdir,getcwd,sep
from troubleshooting.framework.modules.Import import Import
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.variable.variable import  *
from troubleshooting.framework.output.Print import CONSOLE
import sys
RUN_FOLDER = getcwd()

class Builder(object):
    def __init__(self):
        super(Builder,self).__init__()
        self.Import = Import()
        self.logger = logger()
        self.Manager = None
        self.import_dict = None
    def list_python_file_by_path(self,path):
        file_list = listdir(path)
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
            packageName = "%s.%s"%(self.import_dict.split(sep)[-1],pyFile[:-3])
            className = "%s"%pyFile[:-3]
            Object = self.Import.importClass(packageName,className)
            self.Manager.register(Object)
        self.logger.debug("%s be registered keyWord :%s"%(self.Manager.__class__.__name__,[method for method in self.Manager.get_keyword()]))

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

class RecoveryBuilder(Builder):
    def __init__(self,folder):
        super(RecoveryBuilder,self).__init__()
        self.import_dict = folder
        self.Manager = ManagerFactory().getManager(LAYER.Recovery)


class BuilderFactory(object):
    def __init__(self):
        super(BuilderFactory,self).__init__()
    def getBuilder(self,name):
        search_dir = join(RUN_FOLDER,name.value)
        if name == LAYER.KeyWords:
            return KeywordBuilder(search_dir)
        elif name ==  LAYER.TestPoint:
            return TestPointBuilder(search_dir)
        elif name == LAYER.Case:
            return  CaseBuilder(search_dir)
        elif name == LAYER.Recovery:
            return RecoveryBuilder(search_dir)
        else :
            return  None

