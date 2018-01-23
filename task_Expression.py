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

        #for every image it will check whether a face is detected
        if not image.facial_landmarks_error:
            image.matching_results["Expression"] =  _checkExpression(image, image.facial_landmarks)
        else:
            image.matching_results["Expression"] = "Failed: Number of detected faces != 1"


def _checkExpression(image, shape):
    #get image data
    image_data = cv2.imread(image.image_path + image.image_name)

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
    #height between point 62 and point 66
    height62_66 = point66[1]-point62[1]
    #set the height62_66 in relation
    mouthOpenFeature = abs(height62_66/height_8_24)
    #check whether the mouth is closed via definition
    if 2*between_lips<=lower_lip:
        #if its true, check with another definition
        if mouthOpenFeature<= 0.043:
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

    #height difference between the right and the left mouth point
    height48_54 = point54[1] - point48[1]
    #set this height in relation
    noSmileFeature = abs(height48_54/height_8_24)
    #height between the right and the middle (upper part) point
    height48_62 = point62[1]-point48[1]
    #set this height in relation
    noSmileFeatureRight = abs(height48_62/height_8_24)
    #height between the left and the middle (upper part) point
    height54_62 = point62[1]-point54[1]
    #set this height in relation
    noSmileFeatureLeft = abs(height54_62/height_8_24)
    #check whether the person smile or has another not neutral expression
    if noSmileFeature <= 0.023:
        if noSmileFeatureRight <=0.041 and noSmileFeatureLeft <=0.041:
            no_smile = True
        else:
            no_smile = False
    else:
        no_smile = False

    #get all landmarks of the right eyebrow (from right to left)
    point17 = (int(shape[17][0]), int(shape[17][1]))
    point18 = (int(shape[18][0]), int(shape[18][1]))
    point19 = (int(shape[19][0]), int(shape[19][1]))
    point20 = (int(shape[20][0]), int(shape[20][1]))
    point21 = (int(shape[21][0]), int(shape[21][1]))
    #get all landmarks of the right eyebrow (from right to left)
    point22 = (int(shape[22][0]), int(shape[22][1]))
    point23 = (int(shape[23][0]), int(shape[23][1]))
    point24 = (int(shape[24][0]), int(shape[24][1]))
    point25 = (int(shape[25][0]), int(shape[25][1]))
    point26 = (int(shape[26][0]), int(shape[26][1]))

    #height difference between point 17 and point 18
    height17_18 = abs(point17[1]-point18[1])
    #height difference between point 18 and point 19
    height18_19 = abs(point18[1]-point19[1])
    #height difference between point 19 and point 20
    height19_20 = abs(point19[1]-point20[1])
    #height difference between point 20 and point 21
    height20_21 = abs(point20[1]-point21[1])
    #get the average between the height difference (right eyebrow)
    averageEyebrowRight = (height17_18+height18_19+height19_20+height20_21)/4
    #set the average in relation
    raisingEyebrowFeatureRight = averageEyebrowRight/height_8_24

    #height difference between point 22 and point 23
    height22_23 = abs(point22[1]-point23[1])
    #height difference between point 23 and point 24
    height23_24 = abs(point23[1]-point24[1])
    #height difference between point 24 and point 25
    height24_25 = abs(point24[1]-point25[1])
    #height difference between point 25 and point 26
    height25_26 = abs(point25[1]-point26[1])
    #get the average between the height difference
    averageEyebrowLeft = (height22_23+height23_24+height24_25+height25_26)/4
    #set the average in relation
    raisingEyebrowFeatureLeft = averageEyebrowLeft/height_8_24

    #check whether the eyebrows are raised or not
    if raisingEyebrowFeatureRight <= 0.0475 and raisingEyebrowFeatureLeft <= 0.0475:
        no_raisingEyebrows = True
    else:
        no_raisingEyebrows = False

    #when all 3 characteristics are true, we have a neutral expression
    if close_mouth == True and no_smile == True and no_raisingEyebrows == True:
        output_text = "Neutral expression"
    #otherwise (when one of the characteristics is false), we have no neutral expression
    elif close_mouth == False:
        output_text = "No neutral expression, because the mouth is open"
    elif no_raisingEyebrows == False:
        output_text = "No neutral expression, because the eyebrows are not correct"
    elif no_smile == False:
        output_text ="No neutral expression"

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
