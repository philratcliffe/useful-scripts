import xml.etree.cElementTree as etree
import xmltodict
import json

fname = "kis.xml"
ELEMENT_LIST = ["INSTITUTION"]

with open(fname) as xml_doc:
    context = etree.iterparse(xml_doc, events=("start", "end"))

    for event, elem in context:
        if event == "start" and elem.tag in ELEMENT_LIST:
            d = xmltodict.parse(etree.tostring(elem))
            print(json.dumps(d, indent=4))
            for child in elem:
                pass
                #print(child.tag, child.text)
                #% (elem.tag, ", ".join(child.tag for child in elem))
        elem.clear()
