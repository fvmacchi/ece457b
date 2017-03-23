
import sys
import xml.etree.ElementTree as ET
import subject

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
    
    reading_sessions = data["readingSession"]
    for readingSession in root.iter(ns+"readingSession"):
        reading_session = subject.ReadingSession(len(reading_sessions))
        reading_sessions.append(reading_session)

        for nodule in readingSession.iter(ns+"unblindedReadNodule"):
            n = subject.Nodule(nodule.find(ns+"noduleID").text)
            characteristics = nodule.find(ns+"characteristics")
            if characteristics is not None:
                malignancy = characteristics.find(ns+"malignancy")
                if malignancy is not None:
                    n.malignancy = malignancy.text
                lobulation = characteristics.find(ns+"lobulation")
                if lobulation is not None:
                    n.lobulation = lobulation.text
                spiculation = characteristics.find(ns+"spiculation")
                if spiculation is not None:
                    n.spiculation = spiculation.text
                calcification = characteristics.find(ns+"calcification")
                if calcification is not None:
                    n.calcification = calcification.text
            reading_session.add_nodule(n)
            n.reading_session = reading_session
            for roi in nodule.iter(ns+"roi"):
                image_uid = roi.find(ns+"imageSOP_UID").text
                edge_map = get_edgeMap(roi, ns)
                nodule_image = subject.NoduleImage(image_uid)
                nodule_image.nodule = n
                nodule_image.set_edge_map(edge_map)
                n.add_image(nodule_image)

    return data

if __name__ == "__main__":
    if len(sys.argv) > 2:
        parse_xml(sys.argv[1])
    else:
        parse_xml("072.xml")


