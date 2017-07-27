import sys
from framework.log.logger import logger
CONSOLE = sys.stdout
sys.stdout = logger()