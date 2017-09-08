# -*- coding: utf-8 -*-
import sys
from troubleshooting.framework.log.logger import logger
CONSOLE = sys.stdout
def redirection():
    sys.stdout = logger()