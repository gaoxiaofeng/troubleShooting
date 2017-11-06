# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template.Recovery import *
@singleton
class touchFile(Recovery):
    """
    To start specific service by smanager.pl.
    """
    def __init__(self):
        super(self.__class__,self).__init__()
    def action(self,*args):
        for file in args:
            command = "touch %s"%file
            stdout = self.execute_command(command)
            print command
            print stdout
        return STATUS.PASS