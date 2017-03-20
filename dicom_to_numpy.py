# Dependencies
# numpy
# matplotlib
# dicom
import os
import dicom
import numpy
from matplotlib import pyplot, cm
from matplotlib.lines import Line2D

import pprint as pp

DICOM_PATH = "./LIDC-IDRI/"


'''
Class to hold the arrays represnting the dicom figures
'''
class DicomArray():

    def __init__(self):
        # arrays that hold the locations of each pixel
        self.x = None
        self.y = None
        self.z = None

        # 3D array of dicoms
        self.dicomArray = None

        # hold the max and min z values
        self.MAX_Z = None
        self.MIN_Z = None

        self.PIXEL_SPACING = None
        self.PIXEL_DIMENSIONS = None

    '''
    Read the dicoms into a numpy array from the path given
    default path: './LIDC-IDRI/'
    '''
    def read_dicom(self, path=DICOM_PATH):
        dicomList = [] # empty list
        for dirName, subdirList, fileList in os.walk(path):
            for fileName in fileList:
                if ".dcm" in fileName.lower():
                    dicomList.append(os.path.join(dirName, fileName))


        referenceDicom = dicom.read_file(dicomList[0])

        self.PIXEL_DIMENSIONS = (int(referenceDicom.Rows), int(referenceDicom.Columns), len(dicomList))
        self.PIXEL_SPACING = (float(referenceDicom.PixelSpacing[0]), float(referenceDicom.PixelSpacing[1]), float(referenceDicom.SliceThickness))

        # Do not scale by the pixel dimensions
        # self.x = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[0]+1)*self.PIXEL_SPACING[0], self.PIXEL_SPACING[0])
        # self.y = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[1]+1)*self.PIXEL_SPACING[1], self.PIXEL_SPACING[1])
        # self.z = numpy.arange(0.0, (self.PIXEL_DIMENSIONS[2]+1)*self.PIXEL_SPACING[2], self.PIXEL_SPACING[2])
        self.z = numpy.arange(0.0, len(dicomList),1) # 0:1:dicoms
        self.x = numpy.arange(0.0, referenceDicom.Rows, 1) # 0:1:rows
        self.y = numpy.arange(0.0, referenceDicom.Columns, 1) # 0:1:columns

        # Initialize array to hold pixel data for each image
        self.dicomArray = numpy.zeros(self.PIXEL_DIMENSIONS[::-1], dtype=referenceDicom.pixel_array.dtype)

        for dicomFile in dicomList:
            ds = dicom.read_file(dicomFile)
            self.dicomArray[dicomList.index(dicomFile),:,:] = ds.pixel_array

        return True

    '''
    Draw a border based on given x and y arrays
    '''
    def drawEdgeMap(self,fig, x, y):
        ax = pyplot.subplot(111)
        line = Line2D(x,y)
        ax.add_line(line)
        pyplot.show()


    '''
    Create the figure for the dicom
    show: open the dicom viewer (default = True)
    '''
    def plot_dicom(self, dicomNumber, show=True):
        fig = pyplot.figure(1, dpi=300)
        ax1 = fig.add_subplot(111)
        pyplot.axes().set_aspect('equal', 'datalim')
        pyplot.set_cmap(pyplot.gray())
        pyplot.pcolormesh(self.x,self.y,self.dicomArray[dicomNumber,:, :])
        if show:
            pyplot.show()
        return fig

if __name__=="__main__":
    d = DicomArray()
    d.read_dicom("./NSCLC-Radiomics/")

