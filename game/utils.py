import xml.etree.ElementTree as ET

#TODO: implement error handling in the case that xml has errors 

def getCoords(xml_string):
    tree = ET.ElementTree(ET.fromstring(xml_string))
    root = tree.getroot()
    # here we can check root.tags for integrity and consistency check 
    return [(child.attrib['row'], child.attrib['col']) for child in root]
    