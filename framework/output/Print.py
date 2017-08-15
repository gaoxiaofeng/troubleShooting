import sys
from framework.log.logger import logger
CONSOLE = sys.stdout
def redirection():
    sys.stdout = logger()