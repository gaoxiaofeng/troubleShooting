# -*- coding: utf-8 -*-
import re
def getRandomString(lengh):
    import random
    source = "abcdefghijklmnopqlstuvwxyz"
    result = []
    for i in range(lengh):
        result.append(random.choice(source))
    return "".join(result)




def parseRule(rule):
    checkPointList = []
    pattern = re.compile(r".*?(\{.+?\}).*",re.S)
    while 1:
        match = pattern.match(rule)
        if match:
            checkPoint =  match.group(1)
            checkPointList.append(checkPoint)
            rule = rule.replace(checkPoint,"")
        else:
            break
    return checkPointList
def parseRecoveryArgs(argsString):
    import re
    recoverStepsParsed = []
    recoverSteps = argsString.split(",")
    pattern = re.compile(r"([\d\w_]+)\(*([^\(\)]*)\)*", re.I)
    for step in recoverSteps:
        match = pattern.match(step)
        if match:
            method = match.group(1)
            args = match.group(2)
            recoverStepsParsed.append({"method":method,"args": args})
    return recoverStepsParsed