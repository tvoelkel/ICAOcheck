import dlib
from PIL import Image
import cv2
import math
import numpy
import sys
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg

from skimage import io

#this function check wheter the expression is neutral
def checkExpression(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)
        if not image.facial_landmarks_error:
            image.matching_results["Expression"] =  _checkExpression(image, image.facial_landmarks)
        else:
            image.matching_results["Expression"] = "Failed: Number of detected faces != 1"

        """
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
        only for testing
        point_a = [2,3]
        point_b = [2,2]
        distance(point_a,point_b)


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
        """

def _checkExpression(image, shape):
    #get image data
    #image_data = mpimg.imread(image.image_path + image.image_name)

    #shape[n][m]: n is the facial landmark from 0 to 67, m is the pixel-coordinate (0 = x-value, 1 = y-value)
    #description of n-values
    #[0 - 16]: Jawline
    #[17 - 21]: Right eyebrow (from model's perspective)
    #[22 - 26]: Left eyebrow
    #[27 - 35]: Nose
    #[36 - 41]: Right eye
    #[42 - 47]: Left eye
    #[48 - 67]: Mouth

    #point of the upper lip (in the middle - lower part)
    point62 = (int(shape[62][0]), int(shape[62][1]))
    #point of the lower lip (in the middle - upper part)
    point66 = (int(shape[66][0]), int(shape[66][1]))
    #point of the lower lip (in the middle - lower part)
    point57 = (int(shape[57][0]), int(shape[57][1]))

    #distance between upper and lower lip
    between_lips = distance(point62,point66)
    #distance between upper and lower part of the lower lip
    lower_lip = distance(point66,point57)

    #lowest face point (middle)
    point8 = (int(shape[8][0]), int(shape[8][1]))
    #highest face point (middle of the left eyebrow)
    point24 = (int(shape[24][0]), int(shape[24][1]))
    #height betwenn point 8 and point 24
    height_8_24 = point8[1]-point24[1]
    #get value of point 62 in relation to the height between 8 and 24
    relPoint62 = height_8_24/point62[1]
    #get value of point 66 in relation to the height between 8 and 24
    relPoint66 = height_8_24/point66[1]

    relHeight_62_66 = relPoint66 - relPoint62

    #check whether the mouth is closed via definition
    if 2*between_lips<=lower_lip:
        #if its true, check with another definition
        if relHeight_62_66 >= -0.017 and relHeight_62_66 <= 0.017:
            close_mouth = True
        else:
            close_mouth = False
    else:
        close_mouth = False

    #left eyebrow (middle point)
    point19 = (int(shape[19][0]), int(shape[19][1]))
    #left eye (middle point)
    point37 = (int(shape[37][0]), int(shape[37][1]))
    #right eyebrow (middle point)
    point24 = (int(shape[24][0]), int(shape[24][1]))
    #right eye (middle point)
    point44 = (int(shape[44][0]), int(shape[44][1]))

    #right mouth point
    point48 = (int(shape[48][0]), int(shape[48][1]))
    #left mouth point
    point54 = (int(shape[54][0]), int(shape[54][1]))

    #if point48[1]==point54[1] or point48[1]+1==point54[1] or point48[1]+2==point54[1] or point48[1]-1==point54[1] or point48[1]-2==point54[1]:
    no_smile = True
    #else:
    #    no_smile = False
    no_raisingEyebrows = True

    #when all 3 characteristics are true, we have a neutral expression
    if close_mouth == True and no_smile == True and no_raisingEyebrows == True:
        output_text = "Neutral expression"
    #otherwise (when one of the characteristics is false), we have no neutral expression
    elif close_mouth == False:
        output_text = "No neutral expression, because the mouth is open"
    elif no_raisingEyebrows == False:
        output_text = "No neutral expression, because the eyebrows are raised"
    elif no_smile == False:
        output_text ="No neutral expression, because the person smile (no 100 percent security)"

    zahl1 = str(point48[0])
    zahl2 = str(point48[1])
    zahl3 = str(point66[0])
    zahl4 = str(point66[1])
    zahl5 = str(point54[0])
    zahl6 = str(point54[1])
    zahl7 = str(relPoint62)
    zahl8 = str(relPoint66)
    zahl9 = str(relPoint66 - relPoint62)
    output_text = output_text + zahl9#zahl7 + "/" +zahl8#+ zahl1 +", "+zahl2 + " / " + zahl3 + ", " + zahl4 + "/" + zahl5 + ", " + zahl6
    #"//" + str(between_lips) + "//" + str(lower_lip)
    return output_text

#this function calculated the difference betwenn two points
def distance(point_a,point_b):
    #get the values x and the y from point_a
    pointa_x = point_a[0]
    pointa_y = point_a[1]
    #get the values x and the y from point_b
    pointb_x = point_b[0]
    pointb_y = point_b[1]

    #euclid distance between point_a and point_b
    dist = math.sqrt(((pointb_x-pointa_x)**2)+((pointb_y-pointa_y)**2))
    return dist
