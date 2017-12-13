from PIL import Image
import cv2
import numpy
from matplotlib import pyplot as plt

import sys
import dlib
from skimage import io
from skimage import color
from skimage import measure


def checkBackground(imagelist):
    for image in imagelist:

       image.matching_results["Background"]=_checkBackground(image)


def _checkBackground(image):

    

    #image_data = cv2.imread(image.image_path + image.image_name , 0)
    #image_edges = cv2.Canny(image_data, 100, 200)
    """
    plt.subplot(121),plt.imshow(image_data,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(image_edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show() 
    """
    
    image_data = cv2.imread(image.image_path + image.image_name , cv2.IMREAD_COLOR)
    image_gray = cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
    image_filter = cv2.Canny(image_gray,10,80)

    image_filter = cv2.dilate(image_filter, None,iterations=10)
    image_filter = cv2.erode(image_filter, None,iterations=10)

    contour_info = []
    _, contours, _= cv2.findContours(image_filter, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    mask = numpy.zeros(image_filter.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    #mask = cv2.dilate(mask, None, iterations=10)
    #mask = cv2.erode(mask, None, iterations=10)
    
    mask_stack = numpy.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = image_data.astype('float32') / 255.0                 #  for easy blending

    masked =  ((1-mask_stack) * img) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 

    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', masked)                                   
    cv2.waitKey()

    
    #cv2.imshow("test",image_filter)
    #cv2.waitKey(0)

    return ""

