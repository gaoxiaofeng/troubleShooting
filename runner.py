import sys
from builder import TestPointBuilder,EngineBuilder,CaseBuilder
from manager import TestPointManager,EngineManager,CaseManager
from log.logger import logger
from output.output import OutPut
import time
import signal

TestPointBuilder().builder()
EngineBuilder().builder()
CaseBuilder().builder()
OUTPUT = OutPut()
OUTPUT.start()
def onsignal_int(a,b):

    OUTPUT.stop()
    print '\nExit'
    sys.exit(0)



signal.signal(signal.SIGINT,onsignal_int)

Logger = logger()
Logger.debug( "Registed Engine: %s"%EngineManager.get_all_keyword())
Logger.debug( "Registed TestPoint: %s"%TestPointManager.get_all_keyword())
Logger.debug( "Registed Case: %s"%CaseManager.get_all_keyword())
for caseName in CaseManager.get_all_keyword():
    CaseManager.run_case(caseName)
Logger.debug("Case Report: %s"  %CaseManager.case_record )
Logger.debug("TestPoint Report : %s"  %TestPointManager.testPoint_record )

time.sleep(2)
OUTPUT.stop()
