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
    def create(self):
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
        self.write_xml(tree)

    def read_xml(self):
        tree = ET.ElementTree()
        tree.parse(self.recordPath)

        return tree
    def change_node_properties(self,nodelist,kv_map):
        for node in nodelist:
            for key in kv_map:
                node.set(key,kv_map.get(key))

    def update_testpoint_status(self,testpointName,updatedStatus="FIXED"):
        tree = self.read_xml()
        all_testpoints_nodes = self.find_nodes(tree,"case/testpoint")
        selected_testpoint_nodes = self.get_nodes_by_properties(all_testpoints_nodes,{"NAME":testpointName})
        self.change_node_properties(selected_testpoint_nodes,{"STATUS":updatedStatus})
        self.delete_error_message(selected_testpoint_nodes)
        self.update_case_status(tree)
        self.write_xml(tree)
    def update_testpoint_log(self,testpointName,Log):
        tree = self.read_xml()
        all_testpoints_nodes = self.find_nodes(tree,"case/testpoint")
        selected_testpoint_nodes = self.get_nodes_by_properties(all_testpoints_nodes,{"NAME":testpointName})
        self.update_nodes_logs(selected_testpoint_nodes,Log)
        self.write_xml(tree)
    def write_xml(self,tree):
        tree.write(self.recordPath,encoding="utf-8",xml_declaration=True)

    def delete_nodes_text(self,nodes):
        for node in nodes:
            node.text = ""
    def update_nodes_logs(self,nodes,log):
        for node in nodes:
            log_nodes = self.find_nodes(node,"LOG")
            for log_node in log_nodes:
                log_node.text = log

    def get_nodes_by_properties(self,nodelist,kv_map):
        result_nodes = []
        for node in nodelist:
            if self.if_match(node,kv_map):
                result_nodes.append(node)
        return result_nodes

    def delete_error_message(self,nodes):
        for node in nodes:
            self.delete_nodes_text(self.find_nodes(node, "IMPACT"))
            self.delete_nodes_text(self.find_nodes(node, "FIXSTEP"))
            self.delete_nodes_text(self.find_nodes(node, "AUTOFIXSTEP"))
            self.delete_nodes_text(self.find_nodes(node, "RCA"))



    def if_match(self,node,kv_map):
        for key in kv_map:
            if node.get(key) != kv_map.get(key):
                return False
        return True

    def find_nodes(self,tree,path):
        return  tree.findall(path)

    def update_case_status(self,tree):
        case_nodes = self.find_nodes(tree,"case")
        for case_node in case_nodes:
            testpoint_status = []
            testpoint_nodes = self.find_nodes(case_node,"testpoint")
            for testpoint_node in testpoint_nodes:
                status = testpoint_node.get("STATUS")
                testpoint_status.append(status)
            if "FAIL" in testpoint_status:
                case_status = "FAIL"
            elif "FIXED" in testpoint_status:
                case_status = "FIXED"
            else:
                case_status = "PASS"

            self.change_node_properties([case_node], {"STATUS": case_status})

