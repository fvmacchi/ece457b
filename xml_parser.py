
import sys
import xml.etree.ElementTree as ET

XML_PATH = "c:/ece457b/LIDC-IDRI/LIDC-IDRI-0003/1.3.6.1.4.1.14519.5.2.1.6279.6001.101370605276577556143013894866/1.3.6.1.4.1.14519.5.2.1.6279.6001.170706757615202213033480003264"

def get_edgeMap(node):
    edges = {"x": [], "y": [], "z": -1}

    edges["z"] = float(node.find("{http://www.nih.gov}imageZposition").text)
    for edgeMap in node.iter("{http://www.nih.gov}edgeMap"):
        edges["x"].append(int(edgeMap.find("{http://www.nih.gov}xCoord").text))
        edges["y"].append(int(edgeMap.find("{http://www.nih.gov}yCoord").text))
    return edges

def parse_xml(fileName=None):
    if not fileName:
        print "XML file name required"
        return False

    ctr = 0
    root = ET.parse(XML_PATH+"/"+fileName).getroot()
    data = {"uid": -1, "readingSession": []}

    for readingSession in root.iter("{http://www.nih.gov}readingSession"):
        rs = {'nodules': []}

        for nodule in readingSession.iter("{http://www.nih.gov}unblindedReadNodule"):
            n = []

            for roi in nodule.iter("{http://www.nih.gov}roi"):
                image_uid = roi.find("{http://www.nih.gov}imageSOP_UID").text
                edge_map = get_edgeMap(roi)
                n.append({'image_uid': image_uid, 'edge_map': edge_map})
            rs['nodules'].append(n)

        data["readingSession"].append(rs)
    return data

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_xml(sys.argv[1])
    else:
        parse_xml("072.xml")


