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

def checkGeometry(imagelist):
    global result_path

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
    headwidth_W= int(shape[16][0]-shape[0][0])
    headlength_L= 2*(shape[8][1] - M[1])

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
    
    '''
    #output of values
    print("A: %i %s" % (imagewidth_A,image.image_name))
    print("B: %i %s" % (imageheight_B,image.image_name))
    print("Mh: %i %s" % (horizontaldistance_Mh,image.image_name))
    print("Mv: %i %s" % (verticaldistance_Mv,image.image_name))
    print("W: %i %s" % (headwidth_W,image.image_name))
    print("L: %i %s" % (headlength_L,image.image_name))
    print("D_exist: %i %s" % (dx,image.image_name))
    print("D_allowed: %i %s" % (difference_allowed,image.image_name))

    print("image: %r %s" % (image_ratio,image.image_name))
    print("hori: %r %s" % (horizontal_ratio,image.image_name))
    print("verti: %r %s" % (vertical_ratio,image.image_name))
    print("headw: %r %s" % (headwidth_ratio,image.image_name))
    print("headl: %r %s" % (headlength_ratio,image.image_name))
    print("headroll: %r %s" % (head_roll,image.image_name))
    '''

    if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
        ausgabe= "ICAO konform"
    else:
        ausgabe="nicht ICAO konform"
    if image_ratio == False:
        ausgabe=ausgabe+", Seitenverhältnis des Bildes nicht korrekt"
    if horizontal_ratio == False or vertical_ratio == False:
        ausgabe=ausgabe+", Gesicht nicht mittig"
    if headwidth_ratio == False:
        ausgabe=ausgabe+", Verhältnis: Kopfbreite/Bildbreite passt nicht"
    if headlength_ratio == False:
        ausgabe=ausgabe+", Verhältnis Kopflänge/Bildlänge passt nicht"
    if head_roll==False:
        ausgabe=ausgabe+", Kopf zu stark gedreht"

    #cut
    if image_ratio == False or horizontal_ratio == False or vertical_ratio == False or headwidth_ratio == False or headlength_ratio == False or head_roll==False:
        cut_img = cut(image_data,imagewidth_A,imageheight_B,horizontaldistance_Mh,verticaldistance_Mv,headwidth_W,headlength_L,difference_allowed,dx,M)
        if cut_img==True:
            y1=array[0]
            y2=array[1]
            x1=array[2]
            x2=array[3]
        
            cutted_img= image_data[y1:y2,x1:x2]
            ausgabe=ausgabe+" || Zuschnitt ist möglich"
            #cutted_img.save(image.image_path[:-1]+"-result\\" + image.image_name+"-cut")
            cv2.imwrite(result_path+"\\" + image.image_name[:-4]+"-cut.jpg", cutted_img)
            #cv2.imshow("cutted", cutted_img)
        else:
            ausgabe=ausgabe+" || Zuschnitt nicht möglich"

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
    
    print("A: %i " % (A))
    print("B: %i " % (B))
    print("Mh: %i " % (Mh))
    print("Mv: %i " % (Mv))
    print("W: %i " % (W))
    print("L: %i " % (L))
    print("D_exist: %i " % (dx))
    print("D_allowed: %i " % (difference_allowed))

    print("image: %r " % (image_ratio))
    print("hori: %r " % (horizontal_ratio))
    print("verti: %r " % (vertical_ratio))
    print("headw: %r " % (headwidth_ratio))
    print("headl: %r " % (headlength_ratio))
    print("headroll: %r " % (head_roll))
    

def cut(image_data,A,B,Mh,Mv,W,L,difference_allowed,dx,M):
    global image_l
    global image_w
    global array
    global ausrichtung
   
    #y1=0
    #y2=int(B)
    #x1=0
    #x2=int(A)
    #new_A=A
    #new_B=B

    new_A=W/0.65
    new_B=L/0.75

    if new_A/new_B <0.74:
        new_A=new_B*0.75
    if new_A/new_B >0.8:
        new_B=new_A/0.79

    new_Mh= Mh-((Mh-new_A/2))
    new_Mv=Mv-((Mv-new_B*0.48))

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
    else:
        #cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx,M)
        new_A=W/0.74
        new_B=L/0.89

        if new_A/new_B <0.74:
            new_A=new_B*0.75
        if new_A/new_B >0.8:
            new_B=new_A/0.79

        new_Mh= Mh-((Mh-new_A/2))
        new_Mv=Mv-((Mv-new_B*0.4))
        
        proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

        if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:           
            x1=int(Mh-new_Mh)
            x2=int(x1+new_A)
            y1=int(Mv-new_Mv)
            y2=int(y1+new_B)
            array[0] = (y1)
            array[1] = (y2)
            array[2] = (x1)
            array[3] = (x2)
            return True
        else:
            return False

    '''    
    if horizontal_ratio == False: 
        #Gesicht nicht mittig 
        if Mh/A<0.45:
            new_A=Mh/0.47

            new_Mh= Mh
            new_Mv= Mv

            if new_A/B <0.74:   
                new_B=new_A/0.75
                new_Mh= new_Mh
                new_Mv= new_Mv-((B-new_B)/2)
            
            if new_A/B >0.8:   
                new_A=0.79*new_B
                new_Mh= new_Mh
                new_Mv= new_Mv

            if L/new_B < 0.6:
                new_B=L/0.61
                new_Mh= new_Mh
                new_Mv= new_Mv-((B-new_B)/2)

            if W/new_A < 0.5:
                new_A=W/0.51
                new_Mh= new_Mh
                new_Mv= new_Mv

            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:           
                x1=0
                #x2=int(image_w-((image_w-new_A)/2))
                x2=int(new_A)
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
        
        if Mh/A>0.55:
            new_A=(A-Mh)/0.47

            new_Mh= Mh-((A-new_A))
            new_Mv= Mv-((B-new_B))

            if new_A/B <0.74:   
                new_B=A/0.75
                new_Mh= new_Mh
                new_Mv= new_Mv-((B-new_B)/2)
            
            if new_A/B >0.8:   
                new_A=0.79*B
                new_Mh= new_Mh-((A-new_A))
                new_Mv= new_Mv

            if L/new_B < 0.6:
                new_B=L/0.61
                new_Mh= new_Mh
                new_Mv= new_Mv-((B-new_B)/2)

            if W/new_A < 0.5:
                new_A=W/0.51
                new_Mh= new_Mh-((A-new_A))
                new_Mv= new_Mv

            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:           
                x1=int((image_w-new_A))
                x2=int(image_w)
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
       
    #if vertical_ratio == False:
        #Gesicht nicht mittig 
    #    if Mv/B<0.3:
    #        ausrichtung="n"
    #        new_B=Mv/0.31
    #    if Mv/B>0.5:
    #        ausrichtung="s"
    #        new_B=(B-Mv)/0.31

    if image_ratio == False:
            #Seitenverhältnis des Bildes nicht korrekt
        if A/B <0.74:
            new_B=A/0.75
            #y1=int((B-new_B)/2)
            #y2=int(B-((B-new_B)/2))
            
            new_Mh= Mh-((A-new_A)/2)
            new_Mv= Mv-((B-new_B)/2)
            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:         
                x1=int((image_w-new_A)/2)
                x2=int(image_w-((image_w-new_A)/2))
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

        if A/B >0.8:
            new_A=0.79*B
            #x1=int((A-new_A)/2)
            #x2=int(A-((A-new_A)/2))
            
            new_Mh= Mh-((A-new_A)/2)
            new_Mv= Mv-((B-new_B)/2)
            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:           
                x1=int((image_w-new_A)/2)
                x2=int(image_w-((image_w-new_A)/2))
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
 

    if headwidth_ratio == False:
        #Verhältnis: Kopfbreite/Bildbreite passt nicht
        if W/A < 0.5:
            new_A=W/0.51
            #x1=int((A-new_A)/2)
            #x2=int(A-((A-new_A)/2))

            new_Mh= int(Mh-((A-new_A)/2))
            new_Mv= int(Mv-((B-new_B)/2))
            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
                x1=int((image_w-new_A)/2)
                x2=int(image_w-((image_w-new_A)/2))
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
    
    if headlength_ratio == False:
        #Verhältnis Kopflänge/Bildlänge passt nicht
        if L/B < 0.6:
            new_B=L/0.61
            #y1=int((B-new_B)/2)
            #y2=int(B-((B-new_B)/2))

            new_Mh= int(Mh-((A-new_A)/2))
            new_Mv= int(Mv-((B-new_B)/2))
            proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

            if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
                x1=int((image_w-new_A)/2)
                x2=int(image_w-((image_w-new_A)/2))
                y1=int((image_l-new_B)/2)
                y2=int(image_l-((image_l-new_B)/2))
                array[0] = (y1)
                array[1] = (y2)
                array[2] = (x1)
                array[3] = (x2)
                return 1
            else:
                cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

    #if head_roll==False:
        #Kopf zu stark gedreht
    '''
    '''
    #calculation of Terms
    #new_Mh= int(Mh-((A-new_A)/2))
    #new_Mv= int(Mv-((B-new_B)/2))

    #proof(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)

    if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True and head_roll==True:
        
        x1=int((image_w-new_A)/2)
        x2=int(image_w-((image_w-new_A)/2))
        y1=int((image_l-new_B)/2)
        y2=int(image_l-((image_l-new_B)/2))
        #print("x1: %i x2: %i y1: %i y2: %i" % (x1,x2,y1,y2))
    '''    
    '''
        if ausrichtung.equals("w"):
            x1=0
            x2=int(image_w-((image_w-new_A)))
            y1=int((image_l-new_B)/2)
            y2=int(image_l-((image_l-new_B)/2))
        if ausrichtung.equals("s"):
            x1=int((image_w-new_A))
            x2=int(image_w)
            y1=int((image_l-new_B)/2)
            y2=int(image_l-((image_l-new_B)/2))
    '''
    '''    
        array[0] = (y1)
        array[1] = (y2)
        array[2] = (x1)
        array[3] = (x2)
        return 1
        
    else:
        cut(image_data,new_A,new_B,new_Mh,new_Mv,W,L,difference_allowed,dx)
    '''      
