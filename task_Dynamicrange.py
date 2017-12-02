from PIL import Image
import cv2
import numpy
from matplotlib import pyplot as plt

import sys
import dlib
from skimage import io

from math import sqrt

def checkDynamicRange(imagelist):
    image.matching_results["Dynamic Range"] = _checkDynamicRange(imagelist)


def _checkDynamicRange(imagelist):
    
    for image in imagelist:
        #load image data
        
        image_data = io.imread(image.image_path + image.image_name)
        
        detector = dlib.get_frontal_face_detector()
        
        
        print("Processing file: {}".format(image.image_path + image.image_name))
        
        dets = detector(image_data,1)
        if len(dets) == 0:
            return "no Face detected"
        if len(dets) > 1:
            return "more than one Face detected"
        

        image_data_np = numpy.asarray(image_data)
        print(image_data_np.shape)

        image_data_np_red = image_data_np[...,0]
        image_data_np_green = image_data_np[...,1]
        image_data_np_blue = image_data_np[...,2]

        image_data_np_red = image_data_np_red[dets[0].top() : dets[0].bottom() , dets[0].left() : dets[0].right()]
        image_data_np_green = image_data_np_green[dets[0].top() : dets[0].bottom() , dets[0].left() : dets[0].right()]
        image_data_np_blue = image_data_np_blue[dets[0].top() : dets[0].bottom() , dets[0].left() : dets[0].right()]

        hist_red = numpy.histogram(image_data_np_red,255)
        hist_green = numpy.histogram(image_data_np_green,255)
        hist_blue = numpy.histogram(image_data_np_blue,255)

       

        count_rgb = {"red":0,"green":0,"blue":0}

        for x in hist_red[0]:
            if x > 0:
                print(x)
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


        if count_rgb["red"] >= 128:
            red = True
        if count_rgb["green"] >= 128:
            green = True
        if count_rgb["blue"] >= 128:
            blue = True
      
        #print(treshold)
        print("Check passed. Red: %.1f Green: %.1f Blue: %.1f" 
                % ((count_rgb["red"]/256)*100 , (count_rgb["green"]/256)*100 ,(count_rgb["blue"]/256)*100))

        if red and green and blue:
            return ("Check passed. Red: %.1f Green: %.1f Blue: %.1f" 
                % ((count_rgb["red"]/256)*100 , (count_rgb["green"]/256)*100 ,(count_rgb["blue"]/256)*100))

        



