from PIL import Image
import cv2
import numpy 
from matplotlib import pyplot as plt

import sys
import dlib
from skimage import io

def checkGeometry(imagelist):
    for image in imagelist:
        #load image data
        #image_data = io.imread(image.image_path + image.image_name)
        
        image_ratio=False
        horizontal_ratio=False
        vertical_ratio=False
        headwidth_ratio=False
        headlength_ratio=False

        #testwerte
        imagewidth_A= 75
        imageheight_B= 100
        horizontaldistance_Mh= 35
        verticaldistance_Mv= 40
        headwidth_W= 40
        headlength_L= 70


        if imagewidth_A/imageheight_B >= 0.74 and imagewidth_A/imageheight_B <= 0.8:
            image_ratio=True
        
       if horizontaldistance_Mh/imagewidth_A >=0.45 and horizontaldistance_Mh/imagewidth_A <=0.55:           
            horizontal_ratio=True

         if verticaldistance_Mv/imageheight_B >=0.3 and verticaldistance_Mv/imageheight_B <=0.5:
            vertical_ratio=True

        if headwidth_W/imagewidth_A >= 0.5 and headwidth_W/imagewidth_A <= 0.75:
            headwidth_ratio=True

        if headlength_L/imageheight_B >= 0.6 and headlength_L/imageheight_B <= 0.9:
            headlength_ratio=True

        

        if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True:
            image.matching_results["Geometry"]="ICAO komform"
        else: image.matching_results["Geometry"]="nicht ICAO komform"