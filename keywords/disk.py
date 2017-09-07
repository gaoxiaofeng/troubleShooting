# -*- coding: utf-8 -*-
from framework.libraries.library import singleton
import re
from keywords._BaseKeyword import _BaseKeyword
@singleton
class Disk(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
        self._diskSize = {}
        self._diskInodes = {}
    def _listSize(self):
        command = "df -hP | awk '{print $5 $NF}'"
        stdout = self.execute_command(command)
        pattern = re.compile(r"(^\d+)%(\S+)",re.I|re.M)
        _list = pattern.findall(stdout)
        __list = []
        for _tuple in _list:
            if len(_tuple) != 2:
                continue
            __tuple = (_tuple[1],_tuple[0])
            __list.append(__tuple)
        self._diskSize = dict(__list)
    def _listInodes(self):
        command = "df -iP | awk '{print $5 $NF}'"
        stdout = self.execute_command(command)
        pattern = re.compile(r"(^\d+)%(\S+)",re.I|re.M)
        _list = pattern.findall(stdout)
        __list = []
        for _tuple in _list:
            if len(_tuple) != 2:
                continue
            __tuple = (_tuple[1],_tuple[0])
            __list.append(__tuple)
        self._diskInodes = dict(__list)
    def _list(self):
        if self._diskInodes == {}:
            self._listInodes()
        if self._diskSize == {}:
            self._listSize()
    def get_disk_usage_size(self):
        self._list()
        return self._diskSize
    def get_disk_usage_inodes(self):
        self._list()
        return self._diskInodes


if __name__ == "__main__":
    disk = Disk()

