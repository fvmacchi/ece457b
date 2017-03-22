
import sys
import xml.etree.ElementTree as ET

def get_edgeMap(node, ns):
    edges = {"x": [], "y": [], "z": -1}

    edges["z"] = float(node.find(ns+"imageZposition").text)
    for edgeMap in node.iter(ns+"edgeMap"):
        edges["x"].append(int(edgeMap.find(ns+"xCoord").text))
        edges["y"].append(int(edgeMap.find(ns+"yCoord").text))
    return edges

def parse_xml(fileName=None):
    if not fileName:
        print "XML file name required"
        return False

    ctr = 0
    root = ET.parse(fileName).getroot()
    data = {"uid": -1, "readingSession": []}
    ns = ""
    if root.tag.find("{") >= 0:
        ns = root.tag[root.tag.find("{"):root.tag.find("}")+1]

    header = root.find(ns+"ResponseHeader")
    data['version'] = header.find(ns+"Version").text
    
    if not data['version'] == '1.8.1':
        print "Warning: xml version not supported: " + str(data['version'])
        return False
    
    for readingSession in root.iter(ns+"readingSession"):
        rs = {'nodules': []}

        for nodule in readingSession.iter(ns+"unblindedReadNodule"):
            n = []

            for roi in nodule.iter(ns+"roi"):
                image_uid = roi.find(ns+"imageSOP_UID").text
                edge_map = get_edgeMap(roi, ns)
                n.append({'image_uid': image_uid, 'edge_map': edge_map})
            rs['nodules'].append(n)

        data["readingSession"].append(rs)
    return data

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_xml(sys.argv[1])
    else:
        parse_xml("072.xml")


