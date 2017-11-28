import dlib
from PIL import Image
import cv2
import math
import numpy
import sys
from matplotlib import pyplot as plt

from skimage import io

#this function check wheter the expression is neutral
def checkExpression(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)
        image_data = io.imread(image.image_path + image.image_name)

        detector = dlib.get_frontal_face_detector()
        predicator = dlib.shape_predictor()
        #win = dlib.image_window()
        #print("Processing file: {}".format(image.image_path + image.image_name))

        #ToDo get the facial landmarks

        # The 1 in the second argument indicates that we should upsample the image
        # 1 time.  This will make everything bigger and allow us to detect more
        # faces.
        dets = detector(image_data, 1)
        print("Number of faces detected: {}".format(len(dets)))
        for i, d in enumerate(dets):
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                i, d.left(), d.top(), d.right(), d.bottom()))
        #win.clear_overlay()
        #win.set_image(image_data)
        #win.add_overlay(dets)
        """only for testing
        point_a = [2,3]
        point_b = [2,2]
        distance(point_a,point_b)
        """

        #only for testing
        close_mouth = True
        no_smile = True
        no_raisingEyebrows = True

        #preparation for close close mouth

        #calculate the between_lips distance and the thick of the lower lip
        #between_lips = distance()
        #lower_lip = distance()

        #check whether the mouth is closed
        #if 2*between_lips<=lower_lip:
        #    close_mouth = True

        #when all 3 characteristics are true, we have a neutral expression
        if close_mouth == True and no_smile == True and no_raisingEyebrows == True:
            image.matching_results["Expression"]="Neutral expression"
        #otherwise (when one of the characteristics is false), we have no neutral expression
        elif close_mouth == False:
            image.matching_results["Expression"]="No neutral expression, because the mouth is open"
        elif no_raisingEyebrows == False:
            image.matching_results["Expression"]="No neutral expression, because the eyebrows are raised"
        elif no_smile == False:
            image.matching_results["Expression"]="No neutral expression, because the person smile (no 100 percent security)"

#this function calculated the difference betwenn two points
def distance(point_a,point_b):
    #get the values x and the y from point_a
    pointa_x = point_a[0]
    pointa_y = point_a[1]
    #get the values x and the y from point_b
    pointb_x = point_b[0]
    pointb_y = point_b[1]

    #euclid distance between point_a and point_b
    dist = math.sqrt(((pointb_x-pointa_x)**2)-((pointb_y-pointa_y)**2))
    return dist
