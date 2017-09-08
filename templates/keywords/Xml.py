# -*- coding: utf-8 -*-
from troubleshooting.framework.libraries.library import singleton
from troubleshooting.framework.template._BaseKeyword import _BaseKeyword
import xml.etree.ElementTree as ET


@singleton
class Xml(_BaseKeyword):
    def __init__(self):
        super(self.__class__,self).__init__()
        self.data = None

    def get_dict_from_xml(self,fileName):
        # deep is 2
        command = "cat %s"%fileName
        data = self.execute_command(command)

        root = ET.fromstring(data)
        dict = {}
        for child in root:
           attrib = child.attrib
           if attrib.has_key("name"):
               name = attrib["name"]
               dict[name] = {}
               for _child in child:
                   _attrib = _child.attrib
                   if _attrib.has_key("name") and _attrib.has_key("value"):
                       _name = _attrib["name"]
                       _value = _attrib["value"]

                       dict[name][_name] = _value
        return  dict



