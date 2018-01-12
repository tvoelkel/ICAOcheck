import dlib
import cv2 as cv
from PIL import Image
import math
import numpy
import sys
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg

def checkGlasses(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)
        #if not image.facial_landmarks_error:
        image.matching_results["Glasses"] =  _checkGlasses(image, image.facial_landmarks)
        #else:
        #    image.matching_results["Glasses"] = "Failed: Number of detected faces != 1"

def _checkGlasses(image,shape):

    checkExistenceOfGlasses(image)
    """

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
    """
    output_text = checkEyeVisibility(image, shape)

    return output_text

def checkExistenceOfGlasses(image):
    #ToDo check whether the person wear glasses or not

    img = cv.imread(image.image_path+image.image_name,0)
    img2 = img.copy()
    template = cv.imread('template.png',0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv.rectangle(img,top_left, bottom_right, 255, 2)
        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)
        plt.show()
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
    counter = 0
    while i<=41:
        right_eye_points[counter] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1
        counter = counter+1

    #get all points of the left eye
    counter = 0
    while i<=47:
        left_eye_points[i] = (int(shape[i][0]), int(shape[i][1]))
        i = i+1
        counter = counter+1

    text = str(right_eye_points[1][0])
    text2 = str(right_eye_points[1][1])
    return text + "/" + text2
