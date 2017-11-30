import cv2
import numpy as  np
import os
import sys
import dlib
import math
from skimage import io

from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import pyplot as mpimg
from scipy import misc

def checkGeometry(imagelist):
    for image in imagelist:
        #load image data
        #image_data = io.imread(image.image_path + image.image_name)
        if not image.facial_landmarks_error:
            image.matching_results["Geometry"] =  _checkGeometry(image, image.facial_landmarks)
        else:
            image.matching_results["Geometry"] = "Failed: Number of detected faces != 1"

def _checkGeometry(image, shape):
    #shape[n][m]: n is the facial landmark from 0 to 67, m is the pixel-coordinate (0 = x-value, 1 = y-value)

    #description of n-values
    #[0 - 16]: Jawline
    #[17 - 21]: Right eyebrow (from model's perspective)
    #[22 - 26]: Left eyebrow
    #[27 - 35]: Nose
    #[36 - 41]: Right eye
    #[42 - 47]: Left eye
    #[48 - 67]: Mouth

    #feature points as illustrated in ICAO lighting restrictions
    leftEyeCenter = (int((shape[43][0] + shape[44][0] + shape[46][0] + shape[47][0]) / 4), int((shape[43][1] + shape[44][1] + shape[46][1] + shape[47][1]) / 4))
    rightEyeCenter = (int((shape[37][0] + shape[38][0] + shape[40][0] + shape[41][0]) / 4), int((shape[37][1] + shape[38][1] + shape[40][1] + shape[41][1]) / 4))
    mouthCenter = (int((shape[62][0] + shape[66][0])/2), int((shape[62][1] + shape[66][1]) / 2))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))

    H = np.array([leftEyeCenter[0] - rightEyeCenter[0], leftEyeCenter[1] - rightEyeCenter[1]])

    V = np.array([mouthCenter[0] - M[0], mouthCenter[1] - M[1]])


    #variables
    image_ratio=False
    horizontal_ratio=False
    vertical_ratio=False
    headwidth_ratio=False
    headlength_ratio=True
    head_roll=False

    image_data = mpimg.imread(image.image_path + image.image_name)

    #testwerte
    '''imagewidth_A= 75
    imageheight_B= 100
    horizontaldistance_Mh= 35
    verticaldistance_Mv= 40
    headwidth_W= 40
    headlength_L= 70'''

    imagewidth_A= int (len(image_data[0])-1)
    imageheight_B= int (len(image_data)-1)
    horizontaldistance_Mh= int((leftEyeCenter[0] + rightEyeCenter[0]) / 2)
    verticaldistance_Mv= int((leftEyeCenter[1] + rightEyeCenter[1]) / 2)
    headwidth_W= int(shape[16][0]-shape[0][0])
    #headlength_L= 70

    #Pose angle requirement of head roll <=5°
    # |Mh-V(x,0)| <= sin(5°)*Mv

    #difference_exist= math.fabs((((mouthCenter[0]-M[0])/(mouthCenter[1]-M[1]))*(-M[1]))+M[0])
    #difference_exist= math.fabs(((M[0]*-mouthCenter[1])+(-mouthCenter[0]*-M[1]))/(-M[1]+mouthCenter[1]))
    difference_allowed= math.fabs(verticaldistance_Mv*math.sin(math.radians(5)))

    dx=math.fabs(mouthCenter[0]-M[0])
    dy=math.fabs(mouthCenter[1]-M[1])
    if dx != 0:
        m=dy/dx
        dy2=M[1]
        dx=dy2/m

    if dx<=difference_allowed:
        head_roll=True

    if imagewidth_A/imageheight_B >= 0.74 and imagewidth_A/imageheight_B <= 0.8:
        image_ratio=True

    if horizontaldistance_Mh/imagewidth_A >=0.45 and horizontaldistance_Mh/imagewidth_A <=0.55:
        horizontal_ratio=True

    if verticaldistance_Mv/imageheight_B >=0.3 and verticaldistance_Mv/imageheight_B <=0.5:
        vertical_ratio=True

    if headwidth_W/imagewidth_A >= 0.5 and headwidth_W/imagewidth_A <= 0.75:
        headwidth_ratio=True

    #if headlength_L/imageheight_B >= 0.6 and headlength_L/imageheight_B <= 0.9:
    #    headlength_ratio=True

    print("A: %i %s" % (imagewidth_A,image.image_name))
    print("B: %i %s" % (imageheight_B,image.image_name))
    print("Mh: %i %s" % (horizontaldistance_Mh,image.image_name))
    print("Mv: %i %s" % (verticaldistance_Mv,image.image_name))
    print("W: %i %s" % (headwidth_W,image.image_name))
    print("D_exist: %i %s" % (dx,image.image_name))
    print("D_allowed: %i %s" % (difference_allowed,image.image_name))

    print("image: %r %s" % (image_ratio,image.image_name))
    print("hori: %r %s" % (horizontal_ratio,image.image_name))
    print("verti: %r %s" % (vertical_ratio,image.image_name))
    print("headw: %r %s" % (headwidth_ratio,image.image_name))
    print("headl: %r %s" % (headlength_ratio,image.image_name))
    print("headroll: %r %s" % (head_roll,image.image_name))

    if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
        return "ICAO komform"
    else: return "nicht ICAO komform"
