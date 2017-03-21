import pprint as pp

from dicom_to_numpy import DicomArray
from xml_parser import *

da = DicomArray()

# uncomment the code for the dataset you want to use:

### NSCLC Dataset
# da.read_dicom("./NSCLC-Radiomics/")
# figure = da.plot_dicom(77)
### -------------

### LIDC Dataset
da.read_dicom("./LIDC-IDRI/")
xml_filename = "072.xml"
data = parse_xml(xml_filename)
uid = data["readingSession"][0]['nodules'][0][0]['image_uid']
d_file = da.find_image_uid(uid)
figure = da.plot_dicom(d_file, False)
if not data:
    print "XML not parsed"
else:
    x = data["readingSession"][0]['nodules'][0][0]['edge_map']["x"]
    y = data["readingSession"][0]['nodules'][0][0]['edge_map']["y"]
    z = data["readingSession"][0]['nodules'][0][0]['edge_map']["z"]
    da.drawEdgeMap(figure, x,y)
### -------------


