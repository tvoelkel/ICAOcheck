from PIL import Image
import cv2
import numpy 
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg

import sys
import dlib
from skimage import io
from skimage import color
from scipy import misc

from math import sqrt

def checkContrast(imagelist):
    for image in imagelist:

       image.matching_results["Contrast"]=_checkContrast(image)


def _checkContrast(image):

        
    image_data = cv2.imread(image.image_path + image.image_name )
    image_gray = cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
    
    contrast_global = (numpy.amax(image_gray) - numpy.amin(image_gray))   
    
    contrast_local = 0.0
        
    M = numpy.asfarray((
	[1/8, 1/8, 1/8],
	[1/8, 0,1/8],
	[1/8,1/8, 1/8]))

    average_neighbors = (cv2.filter2D(image_gray, -1, M)).astype('uint8')
        
    diff = image_gray - average_neighbors

    contrast_local = (1/image_gray.size) * numpy.sum(diff)

    average_deviation = sqrt(numpy.var(image_gray))
       
    print("----------------------------------------")
    print("{} ".format(int(contrast_local)))
    print("{} ".format(contrast_global))
    print("{} ".format(int(average_deviation)))


    return "Ergebnis Kontrast"
