# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import getRandomString,isSublist,compareList,parseRecoveryArgs
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.builder import BuilderFactory
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.log.logger import logger
import sys,os
import traceback
def recovery(args):
    recoverSteps = parseRecoveryArgs(args)
    recoverStepsName = [step["method"] for step in recoverSteps]
    RecoveryManagerInstance = ManagerFactory().getManager(LAYER.Recovery)
    builderfactory = BuilderFactory()
    builderfactory.getBuilder(LAYER.Recovery).builder()
    recoveryList = RecoveryManagerInstance.get_keyword()

    if isSublist(recoveryList, recoverStepsName):
        print "Framework: try to fix problem.</br>"
        for i, step in enumerate(recoverSteps):
            stepName = step["method"]
            stepArgs = step["args"].split(";")
            sys.stdout.write("Framework: step %s.  %20s" % (i + 1, stepName))
            sys.stdout.flush()
            try:
                status = RecoveryManagerInstance.run_recovery(stepName, *stepArgs)
            except Exception, e:
                logger().error(traceback.format_exc())
                status = STATUS.FAIL
                sys.stdout.write("\t[%s]</br>\n" % status)
                sys.stdout.flush()
                print "Framework: ERROR message save in log file.</br>"
            else:
                sys.stdout.write("\t[%s]\n" % status)
                sys.stdout.flush()
            finally:
                if status == STATUS.FAIL:
                    print "Framework: recovery failed!</br>"
                    return
        print "Framework: recovery successfully!</b>"

    else:
        print "Framework: unkown recovery steps : %s</br>" % compareList(recoveryList, recoverStepsName)