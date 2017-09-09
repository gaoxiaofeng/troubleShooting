NOEXIST = "NOEXIST"

LINEMODE = 1
LISTMODE = 2

SingleMode = 1
DetailMode = 2

PROGREES_LENHTH = 50
#
# try:
#     from enum import Enum,unique
#     @unique
#     class LEVEL(Enum):
#         CRITICAL = "critical"
#         NOCRITICAL = "noCritical"
#     @unique
#     class STATUS(Enum):
#         PASS = "PASS"
#         FAIL = "FAIL"
#         NOTRUN = "NOT_RUN"
#     @unique
#     class BEHAVIOR(Enum):
#         CONTINUE = "continue"
#         RUNAGAIN = "runAgain"
#         EXIT = "exit"
#         NEXT = "Next"
#     @unique
#     class COLOUR(Enum):
#         Blue = "\033[36m"
#         Red = "\033[31m"
#         RedFlash = "\033[1;5;31m"
#         Green = "\033[32m"
#         Yellow = "\033[33m"
#         End = "\033[0m"
#         Reverse =  "\33[7m"
#         HighLight = "\033[1;35m"
#     @unique
#     class LAYER(Enum):
#         Case = "case"
#         TestPoint = "testpoint"
#         KeyWords = "keywords"
#     @unique
#     class SECUREMOD(Enum):
#         SECURE = "secure"
#         INSECURE = "insecure"
#         COMPATIBLE = "compatible"
#     @unique
#     class PROXY(Enum):
#         PROXY1 = "proxy-1"
#         PROXY2 = "proxy-2"
#         PROXY3 = "proxy-3"
# except:
#     # python dont support enum lib
#     def enum(**enums):
#         return  type("Enum",(),enums)
#     LEVEL = enum(CRITICAL = "critical",NOCRITICAL = "noCritical")
#     STATUS = enum(PASS = "PASS",FAIL = "FAIL",NOTRUN = "NOT_RUN")
#     BEHAVIOR = enum(CONTINUE = "continue",RUNAGAIN = "runAgain",EXIT = "exit",NEXT = "Next")
#     COLOUR = enum(Blue = "\033[36m",\
#                   Red = "\033[31m",\
#                   RedFlash = "\033[1;5;31m",\
#                   Green = "\033[32m",\
#                   Yellow = "\033[33m",\
#                   End = "\033[0m", \
#                   Reverse="\33[7m", \
#                   HighLight = "\033[1;35m")
#     LAYER = enum(Case = "case",\
#                 TestPoint = "testpoint",\
#                 KeyWords = "keywords")
#     SECUREMOD = enum(SECURE = "secure",\
#         INSECURE = "insecure",\
#         COMPATIBLE = "compatible")
#     PROXY = enum(PROXY1 = "proxy-1",\
#         PROXY2 = "proxy-2",\
#         PROXY3 = "proxy-3")
def enum(**enums):
    return type("Enum", (), enums)


LEVEL = enum(CRITICAL="critical", NOCRITICAL="noCritical")
STATUS = enum(PASS="PASS", FAIL="FAIL", NOTRUN="NOT_RUN")
BEHAVIOR = enum(CONTINUE="continue", RUNAGAIN="runAgain", EXIT="exit", NEXT="Next")
COLOUR = enum(Blue="\033[36m", \
              Red="\033[31m", \
              RedFlash="\033[1;5;31m", \
              Green="\033[32m", \
              Yellow="\033[33m", \
              End="\033[0m", \
              Reverse="\33[7m", \
              HighLight="\033[1;35m")
LAYER = enum(Case="case", \
             TestPoint="testpoint", \
             KeyWords="keywords")
SECUREMOD = enum(SECURE="secure", \
                 INSECURE="insecure", \
                 COMPATIBLE="compatible")
PROXY = enum(PROXY1="proxy-1", \
             PROXY2="proxy-2", \
             PROXY3="proxy-3")
SYSTEM = enum(WINDOWS="windows",\
              LINUX="linux")