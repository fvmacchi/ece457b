import pprint as pp

from dicom_to_numpy import DicomArray
from xml_parser import *

da = DicomArray()
da.read_dicom("./NSCLC-Radiomics/")

data = parse_xml()

figure = da.plot_dicom(77)
# Uncomment for LIDC dataset with edges
# x = data["readingSession"][0][0][0]["x"]
# y = data["readingSession"][0][0][0]["y"]
# z = data["readingSession"][0][0][0]["z"]
# da.drawEdgeMap(figure, x,y)
