# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import getRandomString,isSublist,compareList,parseRecoveryArgs
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.builder import BuilderFactory
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.log.logger import logger
from troubleshooting.framework.output.record import  record
from troubleshooting.framework.modules.configuration import  ConfigManagerInstance
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
        for i, step in enumerate(recoverSteps):
            stepName = step["method"]
            stepArgs = step["args"].split(";")


            try:
                status = RecoveryManagerInstance.run_recovery(stepName, *stepArgs)
            except Exception, e:
                logger().error(traceback.format_exc())
                status = STATUS.FAIL
            finally:
                if status == STATUS.FAIL:
                    break


        if status == STATUS.FAIL:
            print "<p>Recovery Failed!</p>"

        else:
            record().update_testpoint_status(ConfigManagerInstance.config["R_TestPoint"])
            print "<p>Recovery Successfully!</p>"

    else:
        print "Unkown Recovery Steps : %s" % compareList(recoveryList, recoverStepsName)