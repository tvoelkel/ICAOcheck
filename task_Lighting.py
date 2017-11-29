import numpy as np
import dlib
import cv2
import os
import numpy as np

def checkLighting(imagelist):
    for image in imagelist:
        image.matching_results["Lighting"] = _checkLighting(image)

def _checkLighting(image):
    detector = dlib.get_frontal_face_detector()
    #load dlib pre-trained predictor
    predictor = dlib.shape_predictor(getPredictorFilepath("shape_predictor_68_face_landmarks.dat"))

    img = cv2.imread(image.image_path + image.image_name)
    #second parameter defines the level of upscaling
    #the more upscaling, the higher the required computational power
    #returns an array containing a dlib.rectangle for each detected face
    face_rectangle_array = detector(img, 0)

    if len(face_rectangle_array) > 1:
        return "Failed: More than one face detected."
    elif len(face_rectangle_array) == 0:
        return "Failed: No face detected."
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
    chinContainsContour = False
    foreheadContainsContour = False
    rightCheekContainsContour = False
    leftCheekContainsContour = False

    #feature points as illustrated in ICAO lighting restrictions
    leftEyeCenter = (int((shape[43][0] + shape[44][0] + shape[46][0] + shape[47][0]) / 4), int((shape[43][1] + shape[44][1] + shape[46][1] + shape[47][1]) / 4))
    rightEyeCenter = (int((shape[37][0] + shape[38][0] + shape[40][0] + shape[41][0]) / 4), int((shape[37][1] + shape[38][1] + shape[40][1] + shape[41][1]) / 4))
    mouthCenter = (int((shape[62][0] + shape[66][0])/2), int((shape[62][1] + shape[66][1]) / 2))
    M = (int((leftEyeCenter[0] + rightEyeCenter[0]) / 2), int((leftEyeCenter[1] + rightEyeCenter[1]) / 2))

    H = np.array([leftEyeCenter[0] - rightEyeCenter[0], leftEyeCenter[1] - rightEyeCenter[1]])
    IED = np.linalg.norm(H)

    if IED < 90:
        return "Failed: Inner eye distance smaller than 90px."

    V = np.array([mouthCenter[0] - M[0], mouthCenter[1] - M[1]])
    EM = np.linalg.norm(V)
    MP = 0.3 * IED
    iMP = int(MP)
    cheekLevelSpot = (int(M[0] + 0.5 * V[0]), int(M[1] + 0.5 * V[1]))

    #calculate a rectangle tuple (x, y, width, height) for each measurement zone
    foreheadMeasureRect = (int(M[0] - 0.5 * V[0] - MP/2), int(M[1] - 0.5 * V[1] - MP/2), iMP, iMP)
    chinMeasureRect = (int(M[0] + 1.5 * V[0] - MP/2), int(M[1] + 1.5 * V[1] - MP/2), iMP, iMP)
    rightCheekMeasureRect = (int(cheekLevelSpot[0] - 0.5 * H[0] - MP), int(cheekLevelSpot[1] - 0.5 * H[1]), iMP, iMP)
    leftCheekMeasureRect = (int(cheekLevelSpot[0] + 0.5 * H[0]), int(cheekLevelSpot[1] + 0.5 * H[1]), iMP, iMP)

    #get Intensity values for specific channels of all regions
    (blueValues, greenValues, redValues) = intensityCheck(image, (rightCheekMeasureRect, leftCheekMeasureRect, chinMeasureRect, foreheadMeasureRect))

    if len(blueValues) < 3:
        return "Failed:  Not enough homogenous facial zones."
    elif min(blueValues) < 0.5 * max(blueValues) or min(greenValues) < 0.5 * max(greenValues) or min(redValues) < 0.5 * max(redValues):
        return "Failed: Light intensity difference to high."
    else:
        return "Passed."

def intensityCheck(image, rectangles):
    cropList = []
    redVals = []
    blueVals = []
    greenVals = []
    debugDisplayImage = image

    for i in range(0, 4):
        (x, y, w, h) = rectangles[i]
        crop = image[y:y + h, x:x + w]
        cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        #apply Canny Edge detector
        edges = cv2.Canny(cropGray, 50, 200)

        #print(np.count_nonzero(edges))
        #cv2.imshow(str(i), cropGray)

        if np.count_nonzero(edges) < 50:
            blueVals.append(np.mean(crop[:,:,0]))
            greenVals.append(np.mean(crop[:,:,1]))
            redVals.append(np.mean(crop[:,:,2]))

            #debugging
            cv2.rectangle(debugDisplayImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            i = 0
            #debugging
            cv2.rectangle(debugDisplayImage, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #debugging
    #cv2.imshow(str(image), debugDisplayImage)
    return (blueVals, greenVals, redVals)

def shapeToArray(shape):
    #convert dlib shape object to array
    array = np.zeros((68,2), dtype=np.int)

    #iterate over the facial landmarks
    for i in range(0, 68):
        array[i] = (shape.part(i).x, shape.part(i).y)

    return array
