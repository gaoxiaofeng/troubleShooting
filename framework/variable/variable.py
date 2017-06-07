
NBI3GC_SIMULATOR_PATH = "/opt/oss/NSN-nbi3gc/simulator"
NBI3GC_BIN_PATH = "/opt/oss/NSN-nbi3gc/bin/smx-clt"
NBI3GC_MF_JACORB_PROPERTIES = "/opt/oss/NSN-nbi3gc/smx/common-conf/orb/jacorb.properties"
NBI3GC_PROXY1_JACORB_PROPERTIES = "/etc/opt/oss/global/NSN-nbi3gc/conf/proxy-1/jacorb.properties"
NBI3GC_PROXY2_JACORB_PROPERTIES = "/etc/opt/oss/global/NSN-nbi3gc/conf/proxy-2/jacorb.properties"
NBI3GC_PROXY3_JACORB_PROPERTIES = "/etc/opt/oss/global/NSN-nbi3gc/conf/proxy-3/jacorb.properties"
JACORB_PROPERTIES = "/opt/JacORB/classes/jacorb.properties"
NBI3GC_SIMULATOR_PROPERTIES = "/opt/oss/NSN-nbi3gc/simulator/etc/jacorb.properties"

PRINT_AMARANTH = "\033[35m"
PRINT_BLUE = "\033[36m"
PRINT_RED = "\033[31m"
PRINT_RED_FLASH = "\033[1;5;31m"
PRINT_FLASH = "\033[5m"
PRINT_GREEN = "\033[32m"
PRINT_GREEN_BLOD = "\033[1;32m"
PRINT_YELLOW = "\033[33m"
PRINT_REVERSE = "\33[7m"
PRINT_END = "\033[0m"
PRINT_HIGHLIGHT = "\033[43;30m"
PRINT_HIGHLIGHT = "\033[1;35m"
PRINT_BOLD = "\033[1m"
#PRINT_PASS = PRINT_GREEN +  PASS + PRINT_END
#PRINT_FAIL = PRINT_RED + FAIL + PRINT_END

NOEXIST = "NOEXIST"

LINEMODE = 1
LISTMODE = 2

SingleMode = 1
DetailMode = 2

PROGREES_LENHTH = 50

try:
    from enum import Enum,unique
    @unique
    class LEVEL(Enum):
        CRITICAL = "critical"
        NOCRITICAL = "noCritical"
    @unique
    class STATUS(Enum):
        PASS = "PASS"
        FAIL = "FAIL"
        NOTRUN = "NOT_RUN"
    @unique
    class BEHAVIOR(Enum):
        CONTINUE = "continue"
        RUNAGAIN = "runAgain"
        EXIT = "exit"
        NEXT = "Next"

except:
    # python dont support enum lib
    def enum(**enums):
        return  type("Enum",(),enums)
    LEVEL = enum(CRITICAL = "critical",NOCRITICAL = "noCritical")
    STATUS = enum(PASS = "PASS",FAIL = "FAIL",NOTRUN = "NOT_RUN")
    BEHAVIOR = enum(CONTINUE = "continue",RUNAGAIN = "runAgain",EXIT = "exit",NEXT = "Next")