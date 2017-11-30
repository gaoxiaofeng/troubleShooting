# -*- coding: utf-8 -*-
def isSublist(parentlist,sublist):
    for elem in sublist:
        if elem not in parentlist:
            return False
    return True
def compareList(left,right):
    diff = []
    for elem in right:
        if elem not in left:
            diff.append(elem)
    return diff

def list2stringAndFormat(List):
    result = []
    for i,line in enumerate(List):
        i += 1
        line = "%s. %s"%(i,line)
        result.append(line)
    return "\n".join(result)

def RemoveDuplicates(list):
    finalList = []
    for elem in list:
        if elem not in finalList:
            finalList.append(elem)
    return finalList
