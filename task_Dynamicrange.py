from PIL import Image
import cv2
<<<<<<< HEAD
#from matplotlib import pyplot as plt
=======
import numpy 
from matplotlib import pyplot as plt

import sys
import dlib
from skimage import io

>>>>>>> 3b09df50b2f3abe480b54221686cafa0c24c8194

def checkDynamicRange(imagelist):
    
    for image in imagelist:
<<<<<<< HEAD
        image_data = cv2.imread(image.image_path + image.image_name,0)
        """color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([image_data],[i])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.show()
        """
        image.matching_results["Dynamic Range"]= image_data
=======
        #load image data
        image_data = io.imread(image.image_path + image.image_name)
        
        detector = dlib.get_frontal_face_detector()
        win = dlib.image_window()

        
        print("Processing file: {}".format(image.image_path + image.image_name))
        
        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        dets = detector(image_data, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for i, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                i, d.left(), d.top(), d.right(), d.bottom()))
        win.clear_overlay()
        win.set_image(image_data)
        win.add_overlay(dets)
       
            

        
        face_mask = numpy.zeros(image_data.shape[:2] , numpy.uint8)
        face_mask[ dets[0].top() : dets[0].bottom() , dets[0].left() : dets[0].right() ] = 255

        color = ('r','g','b')
        hist = []
        for i,col in enumerate(color):
            hist_color = cv2.calcHist([image_data],[i],face_mask,[256],[0,256])
            plt.plot(hist_color,color = col)
            plt.xlim([0,256])
            hist.append(hist_color)

        plt.show()
         
        image.matching_results["Dynamic Range"]= "test"
        



>>>>>>> 3b09df50b2f3abe480b54221686cafa0c24c8194
