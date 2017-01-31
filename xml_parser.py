import pprint as pp

import sys
import xml.etree.ElementTree as ET

def get_edgeMap(node):
    edges = {"x": [], "y": [], "z": -1}

    edges["z"] = float(node.find("{http://www.nih.gov}imageZposition").text)
    for edgeMap in node.iter("{http://www.nih.gov}edgeMap"):
        edges["x"].append(int(edgeMap.find("{http://www.nih.gov}xCoord").text))
        edges["y"].append(int(edgeMap.find("{http://www.nih.gov}yCoord").text))
    return edges


def main(fileName="158.xml"):

    ctr = 0
    root = ET.parse(fileName).getroot()
    data = {"uid": -1, "readingSession": []}

    for readingSession in root.iter("{http://www.nih.gov}readingSession"):
        rs = []

        for nodule in readingSession.iter("{http://www.nih.gov}unblindedReadNodule"):
            n = []

            for roi in nodule.iter("{http://www.nih.gov}roi"):
                test = get_edgeMap(roi)
                n.append(test)
            rs.append(n)

        data["readingSession"].append(rs)
    # pp.pprint(data)

if __name__ == "__main__":
    print str(sys.argv)
    if len(sys.argv) > 2:
        main(sys.argv[1])
    else:
        main()
