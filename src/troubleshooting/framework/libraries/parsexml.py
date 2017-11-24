import xml.etree.ElementTree as ET
class parsexml(object):
    def __init__(self):
        super(parsexml,self).__init__()

    def read_xml(self,path):
        tree = ET.ElementTree()
        tree.parse(path)
        return tree

    def find_nodes(self,tree,path):
        return  tree.findall(path)
    def get_cases_status(self,path):
        pass_num = 0
        fail_num = 0
        try:
            tree = self.read_xml(path)
        except Exception,e:
            return 0,0
        case_nodes = self.find_nodes(tree,"case")
        for case_node in case_nodes:
            status = case_node.get("STATUS")
            if status == "FAIL":
                fail_num += 1
            elif status == "FIXED":
                pass_num += 1
            else:
                pass_num += 1
        return pass_num,fail_num