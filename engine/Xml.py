import sys,os
from library.library import ExecuteCommond,singleton
from log.logger import logger
import xml.etree.ElementTree as ET


@singleton
class Xml(object):
    def __init__(self):
        super(self.__class__,self).__init__()
    def get_dict_from_xml(self,fileName):
        # deep is 2
        with open(fileName,"r") as f:
            data = f.read()
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



