# Dependencies
# numpy
# matplotlib
# dicom



import os
import dicom
import numpy
from matplotlib import pyplot, cm

path = "./LIDC-IDRI/"

dicomList = [] # empty list
for dirName, subdirList, fileList in os.walk(path):
    for fileName in fileList:
        if ".dcm" in fileName.lower():
            dicomList.append(os.path.join(dirName, fileName))


referenceDicom = dicom.read_file(dicomList[0])
PIXEL_DIMENSIONS = (int(referenceDicom.Rows), int(referenceDicom.Columns), len(dicomList))
PIXEL_SPACING = (float(referenceDicom.PixelSpacing[0]), float(referenceDicom.PixelSpacing[1]), float(referenceDicom.SliceThickness))


x = numpy.arange(0.0, (PIXEL_DIMENSIONS[0]+1)*PIXEL_SPACING[0], PIXEL_SPACING[0])
y = numpy.arange(0.0, (PIXEL_DIMENSIONS[1]+1)*PIXEL_SPACING[1], PIXEL_SPACING[1])
z = numpy.arange(0.0, (PIXEL_DIMENSIONS[2]+1)*PIXEL_SPACING[2], PIXEL_SPACING[2])


dicomArray = numpy.zeros(PIXEL_DIMENSIONS, dtype=referenceDicom.pixel_array.dtype)

for dicomFile in dicomList:
    ds = dicom.read_file(dicomFile)
    dicomArray[:,:,dicomList.index(dicomFile)] = ds.pixel_array


pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x,y,numpy.flipud(dicomArray[:,:, 80]))
pyplot.show()


