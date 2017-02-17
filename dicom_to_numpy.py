# Dependencies
# numpy
# matplotlib
# dicom
import os
import dicom
import numpy
from matplotlib import pyplot, cm
from matplotlib.lines import Line2D


class DicomArray():

    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.dicomArray = None
        self.PIXEL_SPACING = None
        self.PIXEL_DIMENSIONS = None
        self.path = "./LIDC-IDRI/"


    def read_dicom(self):
        dicomList = [] # empty list
        for dirName, subdirList, fileList in os.walk(self.path):
            for fileName in fileList:
                if ".dcm" in fileName.lower():
                    dicomList.append(os.path.join(dirName, fileName))

        referenceDicom = dicom.read_file(dicomList[0])

        self.PIXEL_DIMENSIONS = (int(referenceDicom.Rows), int(referenceDicom.Columns), len(dicomList))
        self.PIXEL_SPACING = (float(referenceDicom.PixelSpacing[0]), float(referenceDicom.PixelSpacing[1]), float(referenceDicom.SliceThickness))

        self.x = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[0]+1)*self.PIXEL_SPACING[0], self.PIXEL_SPACING[0])
        self.y = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[1]+1)*self.PIXEL_SPACING[1], self.PIXEL_SPACING[1])
        self.z = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[2]+1)*self.PIXEL_SPACING[2], self.PIXEL_SPACING[2])
        # print self.z
        # raw_input()

        self.dicomArray = numpy.zeros(self.PIXEL_DIMENSIONS, dtype=referenceDicom.pixel_array.dtype)

        for dicomFile in dicomList:
            # print dicomFile
            # raw_input()
            ds = dicom.read_file(dicomFile)
            self.dicomArray[:,:,dicomList.index(dicomFile)] = ds.pixel_array

        # ds = dicom.read_file(dicomList[0])
        # self.dicomArray[:,:,dicomList.index(dicomList[0])] = ds.pixel_array

        return True

    def drawEdgeMap(self,fig, x,y):
        # fig = pyplot.figure(1, dpi=300)
        ax = pyplot.subplot(111)
        line = Line2D(x,y)
        ax.add_line(line)
        # ax.set_xlim(min(x), max(x))
        # ax.set_ylim(min(y), max(y))
        # pyplot.pcolormesh(self.x,self.y,numpy.flipud(self.dicomArray[:,:, dicomNumber]))
        # pyplot.show()

        # # ax = pyplot.subplot(111)
        # line = Line2D(x,y)
        # # pyplot.add_line(line)
        # ax1.add_line(line)

        pyplot.show()


    def plot_dicom(self, dicomNumber, x, y):
        fig = pyplot.figure(1, dpi=300)
        ax1 = fig.add_subplot(111)
        pyplot.axes().set_aspect('equal', 'datalim')
        pyplot.set_cmap(pyplot.gray())
        # pyplot.pcolormesh(self.x,self.y,numpy.flipud(self.dicomArray[:,:, dicomNumber]))
        pyplot.pcolormesh(self.x,self.y,self.dicomArray[:,:, dicomNumber])

        return fig

if __name__=="__main__":
    print "This isn't implemented yet"

