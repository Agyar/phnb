import xml.etree.ElementTree as ET

root = ET.Element('data')

for i in range(0,3):
    ET.SubElement(root, 'data').text="IT"

for child in root:
    for i in range(0, 5):
        ET.SubElement(child, 'data').text="WHAT"


for child in root:
    child.attrib = {'pussy':'doh'}
    for c in child:
        c.attrib = {'doh':'pussy'}

tree = ET.ElementTree(root)
tree.write("data_db_test.xml")

load = ET.ElementTree(file="data_db_test.xml")
root = load.getroot()

def run_db(node, meta=None, level=0):
    if node == None:
        return

    if (node.text):
        print("    "*level, node.text, node.attrib)

    for child in node:
        run_db(child, None, level+1)

run_db(root)
