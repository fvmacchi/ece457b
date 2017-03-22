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
        # self.dicomArray = None
        self.dicoms = {}
        self.dicomList = None
        
        self.sliceLocations = {}
        self.image_uids = {}

        # hold the max and min z values
        self.MAX_Z = None
        self.MIN_Z = None

        self.PIXEL_SPACING = None
        self.PIXEL_DIMENSIONS = None
        
        self.FLOAT_HASH_ROUND = 5

    '''
    Read the dicoms into a numpy array from the path given
    default path: './LIDC-IDRI/'
    '''
    def read_dicom(self, path):
        dicomList = [] # empty list
        self.dicomList = dicomList
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
        self.x = numpy.arange(0.0, referenceDicom.Rows, 1) # 0:1:rows
        self.y = numpy.arange(0.0, referenceDicom.Columns, 1) # 0:1:columns

        # Initialize array to hold pixel data for each image
        self.dicomArray = numpy.zeros(self.PIXEL_DIMENSIONS[::-1], dtype=referenceDicom.pixel_array.dtype)

        # for dicomFile in dicomList:
        #     ds = dicom.read_file(dicomFile)
        #     self.dicomArray[dicomList.index(dicomFile),:,:] = ds.pixel_array

        return True
    
    '''
    Find the dicom file with the given z position
    '''
    def find_slice_location(self, position):
        position = round(position, self.FLOAT_HASH_ROUND)
        if not position in self.sliceLocations:
            for dicomFile in self.dicomList:
                ds = dicom.read_file(dicomFile)
                self.sliceLocations[ds.SliceLocation] = dicomFile
                self.image_uids[ds.SOPInstanceUID] = dicomFile
                if position == round(ds.SliceLocation, self.FLOAT_HASH_ROUND):
                    break
        return self.sliceLocations[position]
    
    def find_image_uid(self, uid):
        if not uid in self.image_uids:
            for dicomFile in self.dicomList:
                ds = dicom.read_file(dicomFile)
                self.sliceLocations[ds.SliceLocation] = dicomFile
                self.image_uids[ds.SOPInstanceUID] = dicomFile
                if ds.SOPInstanceUID == uid:
                    break
        return self.image_uids[uid]

    '''
    Draw a border based on given x and y arrays
    '''
    def drawEdgeMap(self, plt, x, y):
        if len(x) == 1 and len(y) == 1:
            circle = plt.Circle((x[0],y[0]),8, ec='b', lw=2, fill=False)
            plt.gcf().gca().add_artist(circle)
        else:
            plt.plot(x,y)
            # ax = plt.subplot(111)
            # line = Line2D(x,y)
            # ax.add_line(line)


    '''
    Create the figure for the dicom
    show: open the dicom viewer (default = True)
    '''
    def plot_dicom(self, plt, dicomFile):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        plt.axes().set_aspect('equal', 'datalim')
        plt.set_cmap(plt.gray())
        plt.pcolormesh(self.x,self.y,self.get_dicom(dicomFile).pixel_array)
    
    '''
    Gets dicom data of the given file
    '''
    def get_dicom(self, dicomFile):
        if not dicomFile in self.dicoms:
            ds = dicom.read_file(dicomFile)
            self.dicoms[dicomFile] = ds
            self.sliceLocations[round(ds.SliceLocation, self.FLOAT_HASH_ROUND)] = dicomFile
            self.image_uids[ds.SOPInstanceUID] = dicomFile
        return self.dicoms[dicomFile]

if __name__=="__main__":
    d = DicomArray()
    d.read_dicom("./NSCLC-Radiomics/")

