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
figure = da.plot_dicom(77, False)
data = parse_xml(xml_filename)
if not data:
    print "XML not parsed"
else:
    x = data["readingSession"][0][0][0]["x"]
    y = data["readingSession"][0][0][0]["y"]
    z = data["readingSession"][0][0][0]["z"]
    da.drawEdgeMap(figure, x,y)
### -------------


