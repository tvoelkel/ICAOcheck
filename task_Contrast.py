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

count = 0


def checkContrast(imagelist):
    global count
    
    countpics=0

    for image in imagelist:
        countpics += 1
        image.matching_results["Contrast"]=_checkContrast(image)
    print("contrast pics:    {}".format(countpics))
    print("contrast conform: {}".format(countpics-count))


def _checkContrast(image):
    global count
        
    #load image data
    image_data = cv2.imread(image.image_path + image.image_name )
    image_gray = cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
    
    #calculate global contrast
    contrast_global = (numpy.amax(image_gray) - numpy.amin(image_gray))
    contrast_global_precentage = contrast_global / 255   
    

    #calculate local contrast
    contrast_local = 0.0
    #get face area
    leftEyeCenter = (int((image.facial_landmarks[43][0] + image.facial_landmarks[44][0] + image.facial_landmarks[46][0] + image.facial_landmarks[47][0]) / 4), int((image.facial_landmarks[43][1] + image.facial_landmarks[44][1] + image.facial_landmarks[46][1] + image.facial_landmarks[47][1]) / 4))
    rightEyeCenter = (int((image.facial_landmarks[37][0] + image.facial_landmarks[38][0] + image.facial_landmarks[40][0] + image.facial_landmarks[41][0]) / 4), int((image.facial_landmarks[37][1] + image.facial_landmarks[38][1] + image.facial_landmarks[40][1] + image.facial_landmarks[41][1]) / 4))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))
    y_hairline = M[1] -  int((image.facial_landmarks[8][1]-M[1])*(2.0/3.0))

    image_gray_face = image_gray[y_hairline : image.facial_landmarks[8][1] , image.facial_landmarks[0][0] : image.facial_landmarks[16][0]]

    #median filter kernel   
    M = numpy.asfarray((
	[1/8, 1/8, 1/8],
	[1/8, 0,1/8],
	[1/8,1/8, 1/8]))

    average_neighbors = (cv2.filter2D(image_gray_face, -1, M)).astype('uint8')  
    diff = image_gray_face - average_neighbors
    contrast_local = int((1/image_gray_face.size) * numpy.sum(diff))

    #calculate average deviation
    average_deviation = int(sqrt(numpy.var(image_gray)))

     #check if the check passed or not
    check = "check passed"
    if (contrast_local <= 60 or average_deviation <= 45 or average_deviation >= 100 or contrast_global <= 200):
        check = "check failed"
        count +=1

   
    result = ("local   {}\nglobal  {}\naverage {}\n\n{} ".format(contrast_local,contrast_global,average_deviation,check)) 
     

    return result
