from PIL import Image, ImageDraw, ImageFilter
import cv2
import numpy
from matplotlib import pyplot as plt

import math

import sys
import dlib
from skimage import io
from skimage import color
from skimage import measure
from skimage import data
from skimage.filters.rank import entropy
from skimage.morphology import disk

from scipy import ndimage


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
    
    image_data = cv2.imread(image.image_path + image.image_name )
    image_gray = cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
    #image_gray = cv2.bilateralFilter(image_gray,9,5,5)
    
    
    """
    mask = numpy.zeros(image_data.shape[:2],numpy.uint8)
    bgdModel = numpy.zeros((1,65),numpy.float64)
    fgdModel = numpy.zeros((1,65),numpy.float64)

    rect = (1,1,image_data.shape[0]-1,image_data.shape[1])
    cv2.grabCut(image_data,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = image_data*mask2[:,:,numpy.newaxis]

    backg = image_data
    backg [mask2 != 0] = 0

    plt.imshow(backg),plt.show()

    """
    """
    my_mask = numpy.zeros(image_data.shape[:2],numpy.uint8)
    #foreground:
    #line between eyes
    my_mask = cv2.line(my_mask,(image.facial_landmarks[0][0],image.facial_landmarks[0][1]),(image.facial_landmarks[16][0],image.facial_landmarks[16][1]),255,10)
    #line from mideye to bottom
    my_mask = cv2.line(my_mask,(image.facial_landmarks[27][0],image.facial_landmarks[27][1]),(image.facial_landmarks[27][0],image_data.shape[1]),255,10)
    #line from 0 to 8

    my_mask = cv2.line(my_mask,(image.facial_landmarks[0][0],image.facial_landmarks[0][1]),(image.facial_landmarks[8][0],image.facial_landmarks[8][1]),255,10)
    #line from 16 to 8
    my_mask = cv2.line(my_mask,(image.facial_landmarks[16][0],image.facial_landmarks[16][1]),(image.facial_landmarks[8][0],image.facial_landmarks[8][1]),255,10)
    #line from 8 to 0 bottom
    my_mask = cv2.line(my_mask,(image.facial_landmarks[8][0],image.facial_landmarks[8][1]),(image.facial_landmarks[0][0],image_data.shape[1]),255,10)
    #line from 8 to 16 bottom
    my_mask = cv2.line(my_mask,(image.facial_landmarks[8][0],image.facial_landmarks[8][1]),(image.facial_landmarks[16][0],image_data.shape[1]),255,10)
    #line from bottom
    my_mask = cv2.line(my_mask,(image.facial_landmarks[0][0],image_data.shape[1]),(image.facial_landmarks[16][0],image_data.shape[1]),255,10)

    #background:
    my_mask = cv2.line(my_mask,(0,0),(0,200),200,int(image_data.shape[0]/10))
    my_mask = cv2.line(my_mask,(image_data.shape[0],0),(image_data.shape[0],200),200,int(image_data.shape[0]/10))
    
    mask[my_mask == 200] = 2
    mask[my_mask == 255] = 1

    bgdModel = numpy.zeros((1,65),numpy.float64)
    fgdModel = numpy.zeros((1,65),numpy.float64)
    mask, bgdModel, fgdModel = cv2.grabCut(image_data,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)

    mask = numpy.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = image_data*mask[:,:,numpy.newaxis]
    plt.imshow(img),plt.colorbar(),plt.show()
    """



    M = numpy.array((
	[-1, -1, -1],
	[-1, 8,-1],
	[-1,-1, -1]), dtype="int")
    N = numpy.array((
	[0, -1, 0],
	[-1,5,-1],
	[0,-1, 0]), dtype="int")

    U =  numpy.asfarray((
	[1.0,4.0,6.0,4.0,1.0],
	[4.0,16.0,24.0,16.0,4.0],
    [6.0,24.0,-476.0,24.0,6.0],
	[4.0,16.0,24.0,16.0,4.0],
	[1.0,4.0,6.0,4.0,1.0]))

    U = U * (-1.0/256.0)


    #image_gray_sharp = (cv2.filter2D(image_gray, -1, U)).astype('uint8')   
    #cv2.namedWindow('imagesharp', cv2.WINDOW_NORMAL)
    #cv2.imshow('imagesharp', image_gray_sharp)             
    
    """
    th = cv2.adaptiveThreshold(image_gray_sharpe,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    th = (255-th)
    th = cv2.erode(th, None,iterations=1)
    image_filter = cv2.dilate(th, None,iterations=1)
    
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.imshow('image', image_filter)                               
    cv2.waitKey()
    """

    image_filter = cv2.Canny(image_gray,10,80)
    
    
    image_filter = cv2.dilate(image_filter, None,iterations=10)
    image_filter = cv2.erode(image_filter, None,iterations=10)

    #cv2.namedWindow('image1', cv2.WINDOW_NORMAL)
    #cv2.imshow('image1', image_filter)      


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
    
    """mask_stack = numpy.dstack([mask]*3)    # Create 3-channel alpha mask

    #-- Blend masked img into MASK_COLOR background --------------------------------------
    mask_stack  = mask_stack.astype('float32') / 255.0          # Use float matrices, 
    img         = image_data.astype('float32') / 255.0                 #  for easy blending

    masked =  ((1-mask_stack) * img) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 
    """
    mask_stack  = mask.astype('float32') / 255.0          # Use float matrices, 
    img         = image_gray.astype('float32') / 255.0                 #  for easy blending

    masked =  ((1-mask_stack) * img) # Blend
    masked = (masked * 255).astype('uint8')                     # Convert back to 8-bit 
    
   
    

    #cv2.namedWindow('image2', cv2.WINDOW_NORMAL)
    #cv2.imshow('image2', masked)             

    
    hist = numpy.histogram(masked,range(1, 256),density=True)
    
    entropy = 0

    for x in hist[0]:
        if (x != 0.0) : entropy = entropy - (x * math.log2(x))

    print(entropy)

    h, w = image_gray.shape[:2]
    #mask_flood = numpy.zeros((h+2, w+2), numpy.uint8)
    mask_flood = numpy.pad(mask,1,mode="constant").astype('uint8') 
    mask_flood = numpy.array_split(mask_flood,2,axis=1)
    mask_flood = numpy.concatenate((mask_flood[1],mask_flood[0]), axis=1)

    #image_gray_split = numpy.hsplit(cv2.bilateralFilter(image_gray,9,5,5),2)
    image_gray_split = numpy.array_split(image_gray,2,axis=1)
    image_gray_split = numpy.concatenate((image_gray_split[1],image_gray_split[0]), axis=1)

    
    
    image_floodfill = image_gray_split.copy()
    # Floodfill from point (0, 0)
    cv2.floodFill(image_floodfill, mask_flood, (int(w/2),0), 0, loDiff=1,upDiff=1 )
    
     
    
    image_floodfill = numpy.array_split(image_floodfill,2,axis=1)
    image_floodfill = numpy.concatenate((image_floodfill[1],image_floodfill[0]), axis=1)
    
    cv2.namedWindow(image.image_name, cv2.WINDOW_NORMAL)
    cv2.imshow(image.image_name, image_floodfill)        


    image_floodfill  = image_floodfill.astype('float32') / 255.0        
    masked         = masked.astype('float32') / 255.0                 

    image_backgroundresult =  (image_floodfill * masked) 
    image_backgroundresult = (image_backgroundresult * 255).astype('uint8')   

    

    #cv2.namedWindow('image4', cv2.WINDOW_NORMAL)
    #cv2.imshow('image4', image_backgroundresult) 
    #cv2.waitKey(0)

    nonzeros = cv2.countNonZero(image_backgroundresult)

    print("{}  {}".format("nonzeros",nonzeros))
    print("percentage {}".format(nonzeros/image_gray.size))


    #TODO: checken wie viele pixel einen unterschied zu einem 10x10 median feld vom hintergrund haben 


    #cv2.imshow("test",image_filter)
    #cv2.waitKey(0)
    cv2.waitKey(0)
    return ""

