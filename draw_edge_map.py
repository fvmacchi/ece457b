import pprint as pp

from dicom_to_numpy import DicomArray as d
from xml_parser import *

da = d()
da.read_dicom()

data = parse_xml()
x = data["readingSession"][0][0][1]["x"]
y = data["readingSession"][0][0][1]["y"]
z = data["readingSession"][0][0][1]["z"]

# print z
print x
raw_input()
print y
raw_input()
figure = da.plot_dicom(66,x,y)
da.drawEdgeMap(figure, x,y)


# Offset = 31.5
# Spacing is 2.5

# 2.5*num + 31.5 = -z
# num = (-1*z-31.5)/2.5


# TODO: We need to figure out a way of determining the z coordinate of the numpy array accurately.
# TODO: With the flipud in plotting, the 0,0 point is bottom left, should be top, left. Figure this out <- Ask Jillian
