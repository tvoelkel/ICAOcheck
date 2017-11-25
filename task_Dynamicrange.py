from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

def checkDynamicRange(imagelist):
    
    for image in imagelist:
        #load image data
        image_data = cv2.imread(image.image_path + image.image_name,0)
        hist = cv2.calcHist([image_data],[0],None,[256],[0,256]) 
        #plt.hist(image_data.ravel(),256,[0,256]); plt.show()
        """
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([image_data],[i],None,[256],[0,256])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.show()
"""
        u = 0
        for x in hist:
            u = u + x
        image.matching_results["Dynamic Range"]= hist



