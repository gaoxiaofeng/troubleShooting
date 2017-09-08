# -*- coding: utf-8 -*-
class Import(object):
    def __init__(self):
        super(Import,self).__init__()
        # self.logger = logger()

    def importClass(self,packageName,className):
        importString = "from %s import %s as Class"%(packageName,className)
        exec importString
        Object = Class()
        return Object
