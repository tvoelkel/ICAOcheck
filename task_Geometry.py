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
from datetime import datetime

#variables
image_ratio=False
horizontal_ratio=False
vertical_ratio=False
headwidth_ratio=False
headlength_ratio=False
head_roll=False
image_w=0
image_l=0
array = np.zeros((4), dtype = np.int)
ausrichtung= "m"
result_path=""
check_cut=0

def checkGeometry(imagelist,Check_Cut):
    global result_path
    global check_cut
    check_cut=Check_Cut
    
    print(str(check_cut))

    if check_cut==1:
        now= datetime.now()
        _now='%s.%s.%s_%s-%s-%s' % (now.day, now.month, now.year, now.hour, now.minute, now.second)
        result_path=imagelist[0].image_path[:-1]+"-result"+str(_now)
        os.mkdir(result_path)

    for image in imagelist:
        #load image data
        #image_data = io.imread(image.image_path + image.image_name)
        if not image.facial_landmarks_error:
            image.matching_results["Geometry"] =  _checkGeometry(image, image.facial_landmarks)
        else:
            image.matching_results["Geometry"] = "Failed: Number of detected faces != 1"

def _checkGeometry(image, shape):
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

    #feature points as illustrated in ICAO lighting restrictions
    leftEyeCenter = (int((shape[43][0] + shape[44][0] + shape[46][0] + shape[47][0]) / 4), int((shape[43][1] + shape[44][1] + shape[46][1] + shape[47][1]) / 4))
    rightEyeCenter = (int((shape[37][0] + shape[38][0] + shape[40][0] + shape[41][0]) / 4), int((shape[37][1] + shape[38][1] + shape[40][1] + shape[41][1]) / 4))
    mouthCenter = (int((shape[62][0] + shape[66][0])/2), int((shape[62][1] + shape[66][1]) / 2))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))

       
    #variables
    global image_ratio
    global horizontal_ratio
    global vertical_ratio
    global headwidth_ratio
    global headlength_ratio
    global head_roll
    global image_w
    global image_l
    global result_path
    
    #calculation of Terms
    imagewidth_A= int (len(image_data[0]))
    imageheight_B= int (len(image_data))
    horizontaldistance_Mh= int((leftEyeCenter[0] + rightEyeCenter[0]) / 2)
    verticaldistance_Mv= int((leftEyeCenter[1] + rightEyeCenter[1]) / 2)
    #headwidth_W= int(shape[16][0]-shape[0][0])
    headwidth_W=int(math.sqrt(((shape[16][0]-shape[0][0])**2)+((shape[16][1]-shape[0][1])**2)))
    #headlength_L= 2*(shape[8][1] - M[1])
    headlength_L=int(2*math.sqrt(((shape[8][0]-M[0])**2)+((shape[8][1]-M[1])**2)))

    image_l=imageheight_B
    image_w=imagewidth_A

    #Pose angle requirement of head roll <=5°
    difference_allowed= math.fabs(verticaldistance_Mv*math.sin(math.radians(5)))
    dx=math.fabs(mouthCenter[0]-M[0])
    dy=math.fabs(mouthCenter[1]-M[1])
    if dx != 0:
        m=dy/dx
        dy2=M[1]
        dx=dy2/m
    
    proof(image_data,imagewidth_A,imageheight_B,horizontaldistance_Mh,verticaldistance_Mv,headwidth_W,headlength_L,difference_allowed,dx)

    if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
        ausgabe= "ICAO konform"
    else:
        ausgabe="nicht ICAO konform"
    if image_ratio == False:
        ausgabe=ausgabe+", \nSeitenverhältnis des Bildes nicht korrekt"
    if horizontal_ratio == False or vertical_ratio == False:
        ausgabe=ausgabe+", \nGesicht nicht mittig"
    if headwidth_ratio == False:
        ausgabe=ausgabe+", \nVerhältnis: Kopfbreite/Bildbreite passt nicht"
    if headlength_ratio == False:
        ausgabe=ausgabe+", \nVerhältnis: Kopflänge/Bildlänge passt nicht"
    if head_roll==False:
        ausgabe=ausgabe+", \nKopf zu stark gedreht"

    #cut
    if image_ratio == False or horizontal_ratio == False or vertical_ratio == False or headwidth_ratio == False or headlength_ratio == False or head_roll==False:
        cut_img = cut(image_data,imagewidth_A,imageheight_B,horizontaldistance_Mh,verticaldistance_Mv,headwidth_W,headlength_L,difference_allowed,dx,M)
        if cut_img==True:
            y1=array[0]
            y2=array[1]
            x1=array[2]
            x2=array[3]
        
            cutted_img= image_data[y1:y2,x1:x2]
            ausgabe=ausgabe+" \n--> Zuschnitt ist möglich"
            if check_cut==1:
                cv2.imwrite(result_path+"\\" + image.image_name[:-4]+"-cut.jpg", cutted_img)
            #cv2.imshow("cutted", cutted_img)
        else:
            ausgabe=ausgabe+" \n--> Zuschnitt nicht möglich"

    return ausgabe

def proof(image_data,A,B,Mh,Mv,W,L,difference_allowed,dx):
    #variables
    global image_ratio
    global horizontal_ratio
    global vertical_ratio
    global headwidth_ratio
    global headlength_ratio
    global head_roll

    #geometric portrait requirement
    if dx<=difference_allowed:
        head_roll=True
    else:
        head_roll=False

    if A/B >= 0.74 and A/B <= 0.8:
        image_ratio=True
    else:
        image_ratio=False

    if Mh/A >=0.45 and Mh/A <=0.55:
        horizontal_ratio=True
    else:
        horizontal_ratio=False

    if Mv/B >=0.3 and Mv/B <=0.5:
        vertical_ratio=True
    else:
        vertical_ratio=False

    if W/A >= 0.5 and W/A <= 0.75:
        headwidth_ratio=True
    else:
        headwidth_ratio=False

    if L/B >= 0.6 and L/B <= 0.9:
        headlength_ratio=True
    else:
        headlength_ratio=False
    

def cut(image_data,A,B,Mh,Mv,W,L,difference_allowed,dx,M):
    global image_l
    global image_w
    global array
    global ausrichtung
   
    for i in range(0,9):
        j=int(i*1.5)
        k=int(i*0.7)

        new_A=W/(0.65+i/10)
        new_B=L/(0.75+j/10)

        if new_A/new_B <0.74:
            new_A=new_B*0.75
        if new_A/new_B >0.8:
            new_B=new_A/0.79

        new_Mh= Mh-((Mh-new_A/2))
        new_Mv=Mv-((Mv-new_B*(0.46-k/10)))

        proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
    
        x1=int(Mh-new_Mh)
        x2=int(x1+new_A)
        y1=int(Mv-new_Mv)
        y2=int(y1+new_B)
    
        if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True and x1>=0 and y1>=0 and x2<=image_w and y2<=image_l:           
            array[0] = (y1)
            array[1] = (y2)
            array[2] = (x1)
            array[3] = (x2)
            return True

    return False
