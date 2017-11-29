import cv2
import numpy as  np
import os
import sys
import dlib
from skimage import io

def checkGeometry(imagelist):
    for image in imagelist:
        #load image data
        #image_data = io.imread(image.image_path + image.image_name)
        
        image_ratio=False
        horizontal_ratio=False
        vertical_ratio=False
        headwidth_ratio=False
        headlength_ratio=False

        #testwerte
        imagewidth_A= 75
        imageheight_B= 100
        horizontaldistance_Mh= 35
        verticaldistance_Mv= 40
        headwidth_W= 40
        headlength_L= 70

        image.matching_results["Geometry"] = _checkGeometry(image)

        if imagewidth_A/imageheight_B >= 0.74 and imagewidth_A/imageheight_B <= 0.8:
            image_ratio=True
        
        if horizontaldistance_Mh/imagewidth_A >=0.45 and horizontaldistance_Mh/imagewidth_A <=0.55:           
            horizontal_ratio=True

        if verticaldistance_Mv/imageheight_B >=0.3 and verticaldistance_Mv/imageheight_B <=0.5:
            vertical_ratio=True

        if headwidth_W/imagewidth_A >= 0.5 and headwidth_W/imagewidth_A <= 0.75:
            headwidth_ratio=True

        if headlength_L/imageheight_B >= 0.6 and headlength_L/imageheight_B <= 0.9:
            headlength_ratio=True

        

        if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True:
            image.matching_results["Geometry"]="ICAO komform"
        else: image.matching_results["Geometry"]="nicht ICAO komform"

def _checkGeometry(image):
    detector = dlib.get_frontal_face_detector()
    #load dlib pre-trained predictor
    predictor = dlib.shape_predictor(getPredictorFilepath("shape_predictor_68_face_landmarks.dat"))

    img = cv2.imread(image.image_path + image.image_name)
    #second parameter defines the level of upscaling
    #the more upscaling, the higher the required computational power
    #returns an array containing a dlib.rectangle for each detected face
    face_rectangle_array = detector(img, 0)

    if len(face_rectangle_array) > 1:
        return "Error: More than one face detected."
    elif len(face_rectangle_array) == 0:
        return "Error: No face detected."
    else:
        shape = shapeToArray(predictor(img, face_rectangle_array[0]))
        return computeImage(img, shape)

def getPredictorFilepath(predictorFilename):
    #for this to work, the facial landmark predictor has to be located inside the same folder as "task_Lightning.py"
    return os.path.realpath(__file__).replace('\\', '/').rsplit('/',1)[0]+'/'+predictorFilename

def computeImage(image, shape):
    #shape[n][m]: n is the facial landmark from 0 to 67, m is the pixel-coordinate (0 = x-value, 1 = y-value)

    #description of n-values
    #[0 - 16]: Jawline
    #[17 - 21]: Right eyebrow (from model's perspective)
    #[22 - 26]: Left eyebrow
    #[27 - 35]: Nose
    #[36 - 41]: Right eye
    #[42 - 47]: Left eye
    #[48 - 67]: Mouth

    #variables
    #feature points as illustrated in ICAO lighting restrictions
    leftEyeCenter = (int((shape[43][0] + shape[44][0] + shape[46][0] + shape[47][0]) / 4), int((shape[43][1] + shape[44][1] + shape[46][1] + shape[47][1]) / 4))
    rightEyeCenter = (int((shape[37][0] + shape[38][0] + shape[40][0] + shape[41][0]) / 4), int((shape[37][1] + shape[38][1] + shape[40][1] + shape[41][1]) / 4))
    mouthCenter = (int((shape[62][0] + shape[66][0])/2), int((shape[62][1] + shape[66][1]) / 2))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))

    H = np.array([leftEyeCenter[0] - rightEyeCenter[0], leftEyeCenter[1] - rightEyeCenter[1]])
    IED = np.linalg.norm(H)

    if IED < 90:
        return "Failed: Inner eye distance smaller than 90px"

    V = np.array([mouthCenter[0] - M[0], mouthCenter[1] - M[1]])
    EM = np.linalg.norm(V)
    MP = 0.3 * IED
    iMP = int(MP)
    cheekLevelSpot = (int(M[0] + 0.5 * V[0]), int(M[1] + 0.5 * V[1]))

    image_ratio=False
    horizontal_ratio=False
    vertical_ratio=False
    headwidth_ratio=False
    headlength_ratio=False

    #testwerte
    imagewidth_A= 75
    imageheight_B= 100
    horizontaldistance_Mh= 35
    verticaldistance_Mv= 40
    headwidth_W= 40
    headlength_L= 70


    if imagewidth_A/imageheight_B >= 0.74 and imagewidth_A/imageheight_B <= 0.8:
        image_ratio=True
        
    if horizontaldistance_Mh/imagewidth_A >=0.45 and horizontaldistance_Mh/imagewidth_A <=0.55:           
        horizontal_ratio=True

    if verticaldistance_Mv/imageheight_B >=0.3 and verticaldistance_Mv/imageheight_B <=0.5:
        vertical_ratio=True

    if headwidth_W/imagewidth_A >= 0.5 and headwidth_W/imagewidth_A <= 0.75:
        headwidth_ratio=True

    if headlength_L/imageheight_B >= 0.6 and headlength_L/imageheight_B <= 0.9:
        headlength_ratio=True
        
    if image_ratio == True and horizontal_ratio == True and vertical_ratio == True and headwidth_ratio == True and headlength_ratio == True:
        return "ICAO komform"
    else: return "nicht ICAO komform"

def shapeToArray(shape):
    #convert dlib shape object to array
    array = np.zeros((68,2), dtype=np.int)

    #iterate over the facial landmarks
    for i in range(0, 68):
        array[i] = (shape.part(i).x, shape.part(i).y)

    return array