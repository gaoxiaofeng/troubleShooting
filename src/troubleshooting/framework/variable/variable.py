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
    @unique
    class COLOUR(Enum):
        Blue = "\033[36m"
        Red = "\033[31m"
        RedFlash = "\033[1;5;31m"
        Green = "\033[32m"
        Yellow = "\033[33m"
        End = "\033[0m"
        Reverse =  "\33[7m"
        HighLight = "\033[1;35m"
    @unique
    class LAYER(Enum):
        Case = "case"
        TestPoint = "testpoint"
        KeyWords = "keywords"
        Recovery = "recovery"
    @unique
    class SYSTEM(Enum):
        WINDOWS = "windows"
        LINUX = "linux"

except:
    class Value(object):
        def __init__(self,value):
            super(Value,self).__init__()
            self.value = value
    class enum(object):
        def __init__(self,**kwargs):
            super(enum,self).__init__()
            # self.__dict__.update(kwargs)
            for key in kwargs:
                self.__dict__.update({key:Value(kwargs[key])})
        def __getattr__(self, item):
            if self.__dict__.has_key(item):
                return self.__dict__[item]
            else:
                print self.__dict__
                raise AttributeError()





    #
    # def enum(**enums):
    #     return type("Enum", (), enums)


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
                KeyWords="keywords", \
                Recovery="recovery")

    SYSTEM = enum(WINDOWS="windows",\
                LINUX="linux")

if __name__ == "__main__":
    pass