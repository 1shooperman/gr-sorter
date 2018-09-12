# pylint: skip-file 
import os
import xml.etree.ElementTree as ElementTree

def get_element(file, xpath):
    xml_file = os.path.abspath(file)
    with open(xml_file, 'r') as myfile:
        data = myfile.read()

    myfile.close()

    root = ElementTree.fromstring(data)
    elem = root.find(xpath)

    if elem != None:
        return elem.text
    else:
        return None

def get_file_as_string(file):
    xml_file = os.path.abspath(file)
    with open(xml_file, 'r') as myfile:
        data = myfile.read()

    myfile.close()

    return data
