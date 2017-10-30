# -*- coding: utf-8 -*-
from troubleshooting.framework.modules.manager import ManagerFactory
from troubleshooting.framework.variable.variable import *
from troubleshooting.framework.modules.configuration import ConfigManagerInstance
from troubleshooting.framework.libraries.system import createDir
import xml.etree.ElementTree as ET
from os.path import dirname,abspath,join
import shelve
class record(object):
    def __init__(self):
        super(record,self).__init__()
        self.caseResult = ManagerFactory().getManager(LAYER.Case).case_record
        self.recordPath = join(ConfigManagerInstance.config["__ProjectCWD__"],"www",ConfigManagerInstance.config["__ReportHash__"],"data.xml")
    def write(self):
        createDir(dirname(self.recordPath))
        root = ET.Element("root")
        for caseName in self.caseResult:
            caseStatus = "PASS" if self.caseResult[caseName]["STATUS"] else "FAIL"
            NoCriticalImpact = "&&".join(self.caseResult[caseName]["IMPACT"]["NoCriticalImpact"])
            CriticalImpact = "&&".join(self.caseResult[caseName]["IMPACT"]["CriticalImpact"])
            DESCRIPTION = self.caseResult[caseName]["DESCRIPTION"]
            REFERENCE = self.caseResult[caseName]["REFERENCE"]
            CASELEVEL =  self.caseResult[caseName]["LEVEL"].value
            TAGS = self.caseResult[caseName]["TAGS"]
            case = ET.SubElement(root, "case",attrib = {"NAME":caseName,"STATUS":caseStatus,"LEVEL":CASELEVEL})
            C_NoCriticalImpact = ET.SubElement(case,"NoCriticalImpact")
            C_NoCriticalImpact.text = NoCriticalImpact
            C_CriticalImpact = ET.SubElement(case,"CriticalImpact")
            C_CriticalImpact.text = CriticalImpact
            C_DESCRIPTION = ET.SubElement(case,"DESCRIPTION")
            C_DESCRIPTION.text = DESCRIPTION
            C_REFERENCE = ET.SubElement(case,"REFERENCE")
            C_REFERENCE.text = REFERENCE
            C_TAGS = ET.SubElement(case,"TAGS")
            C_TAGS.text = TAGS
            TESTPOINT =  self.caseResult[caseName]["TESTPOINT"]
            for testpointName in TESTPOINT:
                STATUS = "PASS" if TESTPOINT[testpointName]["STATUS"] else "FAIL"
                IMPACT = "&&".join(TESTPOINT[testpointName]["IMPACT"])
                DESCRIBE =  TESTPOINT[testpointName]["DESCRIBE"]
                FIXSTEP = "&&".join(TESTPOINT[testpointName]["FIXSTEP"])
                LOG = TESTPOINT[testpointName]["LOG"]
                TIMEOUT = TESTPOINT[testpointName]["TIMEOUT"]
                LEVEL = TESTPOINT[testpointName]["LEVEL"].value
                COST = TESTPOINT[testpointName]["COST"]
                AUTOFIXSTEP = "&&".join(TESTPOINT[testpointName]["AUTOFIXSTEP"])
                RCA = "&&".join(TESTPOINT[testpointName]["RCA"])

                testpoint = ET.SubElement(case,"testpoint",attrib={"NAME":testpointName.strip("{}"),"STATUS":STATUS,"LEVEL":LEVEL})
                T_IMPACT = ET.SubElement(testpoint,"IMPACT")
                T_IMPACT.text = IMPACT
                T_DESCRIBE = ET.SubElement(testpoint,"DESCRIBE")
                T_DESCRIBE.text = DESCRIBE
                T_FIXSTEP = ET.SubElement(testpoint,"FIXSTEP")
                T_FIXSTEP.text = FIXSTEP
                T_LOG = ET.SubElement(testpoint,"LOG")
                T_LOG.text = LOG
                T_TIMEOUT = ET.SubElement(testpoint,"TIMEOUT")
                T_TIMEOUT.text = TIMEOUT
                T_COST = ET.SubElement(testpoint,"COST")
                T_COST.text = COST
                T_AUTOFIXSTEP = ET.SubElement(testpoint,"AUTOFIXSTEP")
                T_AUTOFIXSTEP.text = AUTOFIXSTEP
                T_RCA = ET.SubElement(testpoint,"RCA")
                T_RCA.text = RCA

        tree = ET.ElementTree(root)
        tree.write(self.recordPath)

    def read(self):
        pass


