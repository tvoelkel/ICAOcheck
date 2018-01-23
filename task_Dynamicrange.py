from PIL import Image
import cv2
import numpy
from matplotlib import pyplot as plt

import sys
import dlib
from skimage import io

from math import sqrt

count = 0


def checkDynamicRange(imagelist):

    global count
    countpics = 0

    for image in imagelist:
        countpics += 1
        image.matching_results["Dynamic Range"] = _checkDynamicRange(image)

    print("dynamic range pics:    {}".format(countpics))
    print("dynamic range conform: {}".format(countpics-count))

def _checkDynamicRange(image):
    
    global count

    #load image data 
    image_data = io.imread(image.image_path + image.image_name)
    image_data_np = numpy.asarray(image_data)

    #get face area
    leftEyeCenter = (int((image.facial_landmarks[43][0] + image.facial_landmarks[44][0] + image.facial_landmarks[46][0] + image.facial_landmarks[47][0]) / 4), int((image.facial_landmarks[43][1] + image.facial_landmarks[44][1] + image.facial_landmarks[46][1] + image.facial_landmarks[47][1]) / 4))
    rightEyeCenter = (int((image.facial_landmarks[37][0] + image.facial_landmarks[38][0] + image.facial_landmarks[40][0] + image.facial_landmarks[41][0]) / 4), int((image.facial_landmarks[37][1] + image.facial_landmarks[38][1] + image.facial_landmarks[40][1] + image.facial_landmarks[41][1]) / 4))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))

    y_hairline = M[1] -  int((image.facial_landmarks[8][1]-M[1])*(2.0/3.0))

    image_data_np = image_data_np[y_hairline : image.facial_landmarks[8][1] , image.facial_landmarks[0][0] : image.facial_landmarks[16][0]]

    #split pictures into color chanels
    image_data_np_red = image_data_np[...,0]
    image_data_np_green = image_data_np[...,1]
    image_data_np_blue = image_data_np[...,2]

    #get histogram
    hist_red = numpy.histogram(image_data_np_red,range(0, 256))
    hist_green = numpy.histogram(image_data_np_green,range(0, 256))
    hist_blue = numpy.histogram(image_data_np_blue,range(0, 256))

    
    #check dynamic range
    count_rgb = {"red":0,"green":0,"blue":0}

    for x in hist_red[0]:
        if x > 0:
            count_rgb["red"] = count_rgb["red"] + 1
    for x in hist_green[0]:
        if x > 0:
            count_rgb["green"] = count_rgb["green"] + 1
    for x in hist_blue[0]:
        if x > 0:
            count_rgb["blue"] = count_rgb["blue"] + 1
      
    red = False
    green = False
    blue = False


    #check if dynamic range over 50%
    if count_rgb["red"] >= 128:
        red = True
    if count_rgb["green"] >= 128:
        green = True
    if count_rgb["blue"] >= 128:
        blue = True
      

    if red and green and blue:
        return ("Check passed.\n Red: %.1f %%\n Green: %.1f %%\n Blue: %.1f %%\n Intesity Variation" 
            % ((count_rgb["red"]/256)*100 , (count_rgb["green"]/256)*100 ,(count_rgb["blue"]/256)*100))
    else:
        count += 1
        message = "Check failed.\n"
        if not red:
            message += ("Red only %.1f %%\n" % ((count_rgb["red"]/256)*100))
        else:
            message += ("Red: %.1f %%\n" % ((count_rgb["red"]/256)*100))
        if not green:
            message += ("Green only %.1f %%\n" % ((count_rgb["green"]/256)*100))
        else:
            message += ("Green: %.1f %%\n" % ((count_rgb["green"]/256)*100))
        if not blue:
            message += ("Blue only %.1f %%\n Intesity Variation" % ((count_rgb["blue"]/256)*100))
        else:
            message += ("Blue: %.1f %%\n Intesity Variation" % ((count_rgb["blue"]/256)*100))

        return message
        

        


        



