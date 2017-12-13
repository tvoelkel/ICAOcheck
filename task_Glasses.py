import dlib
import cv2
from PIL import Image
import math
import numpy
import sys
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg

from skimage import io

def checkGlasses(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)
        if not image.facial_landmarks_error:
            image.matching_results["Glasses"] =  _checkGlasses(image, image.facial_landmarks)
        else:
            image.matching_results["Glasses"] = "Failed: Number of detected faces != 1"

def _checkGlasses(image,shape):

    checkExistenceOfGlasses = True

    if checkExistenceOfGlasses == True:
        glasses = True
        if checkEyeVisibility(image, shape) == True:
            eyes_visibility = True
        else:
            eyes_visibility = False
    else:
        glasses = False

    if glasses == False:
        output_text = "The person does not wear glasses"
    elif glasses == True and eyes_visibility == False:
        output_text = "The person wear glasses and the eyes are not visible"
    elif glasses == True and eyes_visibility == True:
        output_text = "The person wear glasses and the eyes are visible"

    return output_text

    return checkEyeVisibility

def checkExistenceOfGlasses(image):
    #ToDo check whether the person wear glasses or not
    return False

def checkEyeVisibility(image,shape):
    #ToDo check the visibility of the eyes when the person wear glasses
    #get image data
    image_data = mpimg.imread(image.image_path + image.image_name)

    #shape[n][m]: n is the facial landmark from 0 to 67, m is the pixel-coordinate (0 = x-value, 1 = y-value)
    #description of n-values
    #[0 - 16]: Jawline
    #[17 - 21]: Right eyebrow (from model's perspective)
    #[22 - 26]: Left eyebrow
    #[27 - 35]: Nose
    #[36 - 41]: Right eye
    #[42 - 47]: Left eye
    #[48 - 67]: Mouth

    right_eye_points = {}
    left_eye_points = {}
    i = 36
    #get all points of the right eye
    while i<=41:
        point = 'point'+str(i)
        right_eye_points[point] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1

    #get all points of the left eye
    while i<=47:
        point = 'point'+str(i)
        left_eye_points[point] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1

    return False
