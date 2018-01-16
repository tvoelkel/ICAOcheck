import dlib
import cv2

import math
import numpy as np
import sys
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg
from PIL import Image


import numpy as  np
import os
from skimage import io
from scipy import misc


def checkGlasses(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)
        if not image.facial_landmarks_error:
            image.matching_results["Glasses"] =  _checkGlasses(image, image.facial_landmarks)
        else:
            image.matching_results["Glasses"] = "Failed: Number of detected faces != 1"

def _checkGlasses(image,shape):

    #checkExistenceOfGlasses(image)


    if checkExistenceOfGlasses(image) == True:
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

    # if checkEyeVisibility(image, shape) == True:
    #     output_text = "konform"
    # else:
    #     output_text = "nicht konform"
    #
    return output_text

def checkExistenceOfGlasses(image):
    #ToDo check whether the person wear glasses or not

    img = cv2.imread(image.image_path+image.image_name,0)
    img2 = img.copy()
    val = 0

    #templates = {}
    #templates[0] = cv2.imread("C:/Users/Patrick Liedtke/github/ICAOcheck/brille1.jpg",0)#"C:/Users/krusc/Desktop/brille.jpg",0)#'F:/test pictures/template.jpg')#'C:/Users/Patrick Liedtke/github/ICAOcheck/template.jpg')#image.image_path+image.image_name,0)##)#'template.jpg',0)
    #templates[1] = cv2.imread("C:/Users/Patrick Liedtke/github/ICAOcheck/brille2.jpg",0)
    #templates[2] = cv2.imread("C:/Users/Patrick Liedtke/github/ICAOcheck/brille3.jpg",0)
    #templates[3] = cv2.imread("C:/Users/Patrick Liedtke/github/ICAOcheck/brille4.jpg",0)
    template = cv2.imread("C:/Users/Patrick Liedtke/github/ICAOcheck/brille3.jpg",0)
    #for template in templates:
    w, h = img.shape[::-1]
    #template.astype(0)
    # All the 6 methods for comparison in a list
    #methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    #for meth in methods:
    img = img2.copy()
    method = eval('cv2.TM_CCORR_NORMED')
        # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > val:
        val = max_val

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #top_left = max_val#max_loc
    if val >= 0.995:
        return True
    else:
        return False
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv2.rectangle(img,top_left, bottom_right, 255, 2)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.suptitle('cv2.TM_CCORR_NORMED')
    # plt.show()
    # return False

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
    #get all points of the right eye (points 36-41)
    counter = 0
    while i<=41:
        right_eye_points[counter] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1
        counter = counter+1

    #get all points of the left eye (points 42-47)
    counter = 0
    while i<=47:
        left_eye_points[counter] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1
        counter = counter+1

    text = str(right_eye_points[1][0])
    text2 = str(right_eye_points[1][1])

    #lowest face point (middle)
    point8 = (int(shape[8][0]), int(shape[8][1]))
    #highest face point (middle of the left eyebrow)
    point24 = (int(shape[24][0]), int(shape[24][1]))
    #height betwenn point 8 and point 24
    height_8_24 = point8[1]-point24[1]

    #height between point 36 (right point of the right eye) and point 39 (left point of the right eye)
    height36_39 = right_eye_points[0][1]-right_eye_points[3][1]
    #set the height in relation
    rightEyeLeftRightCheck = abs(height36_39/height_8_24)
    #height between point 42 (right point of the left eye) and point 45 (left point of the left eye)
    height42_45 = left_eye_points[0][1]-left_eye_points[3][1]
    #set the height in relation
    leftEyeLeftRightCheck = abs(height42_45/height_8_24)
    #height between point 36 (right point of the right eye) and point 45 (left point of the left eye)
    height36_45 = right_eye_points[0][1]-left_eye_points[3][1]
    #set the height in relation
    bothEyeCheck1 = abs(height36_45/height_8_24)
    #height between point 39 (left point of the right eye) and point 42 (right point of the left eye)
    height39_42 = right_eye_points[3][1]-left_eye_points[0][1]
    #set the height in relation
    bothEyeCheck2 = abs(height39_42/height_8_24)

    if leftEyeLeftRightCheck <= 0.027 and rightEyeLeftRightCheck <= 0.027:
        if bothEyeCheck1 <= 0.037 and bothEyeCheck2 <= 0.023:
            eyes_visibility = True
        else:
            eyes_visibility = False
    else:
        eyes_visibility = False

    #zahl1 = str(rightEyeLeftRightCheck)
    #zahl2 = str(leftEyeLeftRightCheck)
    #zahl3 = str(bothEyeCheck1)
    #zahl4 = str(bothEyeCheck2)
    return eyes_visibility
