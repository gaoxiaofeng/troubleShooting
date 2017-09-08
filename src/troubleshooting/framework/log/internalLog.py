# -*- coding: utf-8 -*-
class internalLog(object):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._content = []
    def write(self,data):
        self._content.append(data)
    def flush(self):
        pass
    def getContent(self):
        return "".join(self._content)
