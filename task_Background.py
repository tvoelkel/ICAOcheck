from PIL import Image, ImageDraw, ImageFilter
import cv2
import numpy
import numpy.ma as ma
from matplotlib import pyplot as plt
import math
import sys
import dlib
from scipy import ndimage


count = 0


def checkBackground(imagelist):
    global count
    countpics=0


    for image in imagelist:
        countpics += 1
        image.matching_results["Background"]=_checkBackground(image)
    
    print("background pics:    {}".format(countpics))
    print("background conform: {}".format(countpics-count))

def _checkBackground(image):
    global count
    
    #read image and convert to gray
    image_data = cv2.imread(image.image_path + image.image_name )
    image_gray = cv2.cvtColor(image_data,cv2.COLOR_BGR2GRAY)
    
    #edge detection
    image_filter = cv2.Canny(image_gray,10,80)
      
    #closing of edges
    image_filter = cv2.dilate(image_filter, None,iterations=10)
    image_filter = cv2.erode(image_filter, None,iterations=10)

    #find longest contour at edges
    #used http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_table_of_contents_contours/py_table_of_contents_contours.html
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

    #create background mask
    mask = numpy.zeros(image_filter.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))
    
    # Use float matrices
    mask_stack  = mask.astype('float32') / 255.0 
    #  for easy blending           
    img         = image_gray.astype('float32') / 255.0    
    # Blend mask with picture
    masked =  ((1-mask_stack) * img) 
    # Convert back to 8-bit
    masked = (masked * 255).astype('uint8')                
    
    #create masked array
    image_gray_masked = ma.masked_array(image_gray,mask_stack)  

    #calculate entropy with histogram
    hist = numpy.histogram(image_gray_masked.compressed(),range(0, 256),density=True)
    entropy = 0
    for x in hist[0]:
        if (x != 0.0) : entropy = entropy - (x * math.log2(x))

    #create mask for floodfill
    h, w = image_gray.shape[:2]
    mask_flood = numpy.pad(mask,1,mode="constant").astype('uint8') 
    mask_flood = numpy.array_split(mask_flood,2,axis=1)
    mask_flood = numpy.concatenate((mask_flood[1],mask_flood[0]), axis=1)

    #split picture vertical, and switch sides
    image_gray_split = numpy.array_split(image_gray,2,axis=1)
    image_gray_split = numpy.concatenate((image_gray_split[1],image_gray_split[0]), axis=1)

    
    
    image_floodfill = image_gray_split.copy()
    # Floodfill from point (0, 0)
    cv2.floodFill(image_floodfill, mask_flood, (int(w/2),0), 0, loDiff=1,upDiff=1 )
    
     
    #calculate how many pixels are not in floodfill and mask
    image_floodfill = numpy.array_split(image_floodfill,2,axis=1)
    image_floodfill = numpy.concatenate((image_floodfill[1],image_floodfill[0]), axis=1)
    image_floodfill  = image_floodfill.astype('float32') / 255.0        
    masked         = masked.astype('float32') / 255.0                 
    image_backgroundresult =  (image_floodfill * masked) 
    image_backgroundresult = (image_backgroundresult * 255).astype('uint8')   

    nonzeros = cv2.countNonZero(image_backgroundresult)


    #compare median from corner with background pixels
    #from 5% left corner
    background_average = int(numpy.average(image_gray[0:int(image_gray.shape[1]*0.05), 0:int(image_gray.shape[1]*0.05)]))
    background_mask = mask.copy()
    background_mask [mask == 0.0] = 255
    background_mask [mask == 255.0] = 0
    background_count = numpy.count_nonzero(background_mask)
    background_mask = background_mask.astype('float32') / 255.0

    background_averagedeviation = ((background_average-50 <= image_gray) & (image_gray <= background_average+50))
    background_averagedeviation[background_averagedeviation==True] = 255 
    background_averagedeviation[background_averagedeviation==False] = 0
    background_averagedeviation.astype('float32') / 255.0
    background_averagedeviation = ((background_averagedeviation*background_mask)*255).astype('uint8')


    background_averagedeviation_count = numpy.count_nonzero(background_averagedeviation) 
    background_inconform_pixels = background_count - background_averagedeviation_count
    background_inconform_pixels_percentage = background_inconform_pixels / image_gray.size

    #check if the check passed or not
    result = "check passed"
    if background_inconform_pixels_percentage > 0.02 :
        if entropy > 1:
            result = "check failed"
            count+=1
    

    return result

