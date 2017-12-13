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

def rgb2gray(rgb):
    return numpy.dot(rgb[...,:3], [0.299, 0.587, 0.114])

def get_neighbor_average(image_data, x, y):
    if  x == 0 or y == 0 or x == (len(image_data)-1) or y == (len(image_data[0])-1):
        return image_data[x][y]
    else:

        # oder vielleicht mit der scipy.ndimage.filters.generic_filter Funktion

        return ((image_data[x-1][y-1] + image_data[x-1][y] + image_data[x-1][y+1] + image_data[x][y-1] + 
            image_data[x][y+1] + image_data[x+1][y-1] + image_data[x+1][y] + image_data[x+1][y+1])/8)

def get_min(image_data):
    minimum = 255.0
    for x in image_data:
        if min(x) < minimum:
            minimum = min(x)
    return minimum

def get_max(image_data):
    maximum = 0.0
    for x in image_data:
        if max(x) > maximum:
            maximum = max(x)
    return maximum

def checkContrast(imagelist):
    for image in imagelist:
        
        #load image data
        
        image_data = io.imread(image.image_path + image.image_name)
        image_data_grey = rgb2gray(image_data)

        

        contrast_local = 0.0

        # counter i and element x
        for i,x in enumerate(image_data_grey):
            for j,y in enumerate(image_data_grey[i]):
                contrast_local = contrast_local + abs(y - get_neighbor_average(image_data_grey,i,j)) 

        contrast_local = (1 / (len(image_data)*len(image_data[0]))) * contrast_local


        

        contrast_global = (get_max(image_data_grey) - get_min(image_data_grey))/(255.0)

        #print("asd %.100f" % (1 / len(image_data)*len(image_data[0])))

        mean_deviation = sqrt(numpy.var(numpy.asarray(image_data_grey)))


        plt.hist(numpy.asarray(image_data_grey), bins=256)  # arguments are passed to np.histogram
        plt.title("Histogram %s" % image.image_name)
        plt.show()

        print("Processing file: {}".format(image.image_path + image.image_name))
        print("Contrast Local: %.2f %s" % (contrast_local,image.image_name))
        print("Contrast Global: %.2f %s" % (contrast_global,image.image_name))
        print(mean_deviation)

        image.matching_results["Contrast"] = "Ergebnis Contrast"
