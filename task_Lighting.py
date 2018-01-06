import numpy as np
import dlib
import cv2
import os
import numpy as np

def checkLighting(imagelist):
    for image in imagelist:
        if not image.facial_landmarks_error:
            image.matching_results["Lighting"] = computeImage(image, image.facial_landmarks)
        else:
            image.matching_results["Lighting"] = "Failed: Number of detected faces != 1"

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

    colorCheck(image, (rightCheekMeasureRect, leftCheekMeasureRect, chinMeasureRect, foreheadMeasureRect))
    if IED < 90:
        return "Failed: Inner eye distance smaller than 90px."

    #get Intensity values for specific channels of all regions
    blueValues, greenValues, redValues, blueLN, greenLN, redLN = intensityCheck(image, (rightCheekMeasureRect, leftCheekMeasureRect, chinMeasureRect, foreheadMeasureRect))

    if (min(blueValues) >= 0.5 * max(blueValues) and min(greenValues) >= 0.5 * max(greenValues) and min(redValues) >= 0.5 * max(redValues)) or (min(blueLN) >= 0.5 * max(blueLN) and min(greenLN) >= 0.5 * max(greenLN) and min(redLN) >= 0.5 * max(redLN) and len(blueLN) > 2):
        return "Passed."
    elif len(blueLN) < 3:
        return "Failed:  Not enough homogeneous facial zones."
    else:
        return "Failed: Light intensity difference too high."

def intensityCheck(image, rectangles):
    cielab_a = []
    cielab_b = []

    cropList = []
    redVals = []
    blueVals = []
    greenVals = []

    redValsLowNoise = []
    blueValsLowNoise = []
    greenValsLowNoise = []

    img = cv2.imread(image.image_path + image.image_name)
    debugDisplayImage = img

    for i in range(0, 4):
        (x, y, w, h) = rectangles[i]
        crop = img[y:y + h, x:x + w]
        cropGray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

        #apply Canny Edge detector
        edges = cv2.Canny(cropGray, 50, 200)

        #print(np.count_nonzero(edges))
        #cv2.imshow(str(i), cropGray)

        blueVals.append(np.mean(crop[:,:,0]))
        greenVals.append(np.mean(crop[:,:,1]))
        redVals.append(np.mean(crop[:,:,2]))

        if np.count_nonzero(edges) < 1.5 * w:
            blueValsLowNoise.append(np.mean(crop[:,:,0]))
            greenValsLowNoise.append(np.mean(crop[:,:,1]))
            redValsLowNoise.append(np.mean(crop[:,:,2]))


            #debugging
            #cv2.rectangle(debugDisplayImage, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            i = 0
            #debugging
            #cv2.rectangle(debugDisplayImage, (x, y), (x + w, y + h), (0, 0, 255), 2)

    #debugging
    #cv2.imshow(str(image), debugDisplayImage)

    #interpret skin values
    #because opencv maps l*a*b* values to 0-255 we have to reconvert them to their normal -127 <= x <= 127 range
    #in this range a should lay between 5-35 and b between 5-35 for a natural skin tone

    return blueVals, greenVals, redVals, blueValsLowNoise, greenValsLowNoise, redValsLowNoise

def colorCheck(image, rectangles):
    cielab_a = []
    cielab_b = []

    img = cv2.imread(image.image_path + image.image_name)
    debugDisplayImage = img

    for i in range(0, 4):
        (x, y, w, h) = rectangles[i]
        crop = img[y:y + h, x:x + w]
        lab_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2LAB)
        l_channel, a_channel, b_channel = cv2.split(lab_crop)

        cielab_a.append(np.mean(a_channel))
        cielab_b.append(np.mean(b_channel))

    #interpret skin tone values
    #because opencv maps l*a*b* values to 0-255 we have to reconvert them to their normal -127 <= x <= 127 range
    #in this range a should lay between 5-35 and b between 5-35 for a natural skin tone
    cielab_a_all_mean = np.mean(cielab_a) - 128
    cielab_b_all_mean = np.mean(cielab_b) - 128

    if cielab_a_all_mean >= 5 and cielab_a_all_mean <=35 and cielab_b_all_mean >= 5 and cielab_a_all_mean <= 35:
        image.matching_results["Color"] = "Passed."
    else:
        image.matching_results["Color"] = "Unnatural skin tone. CIELAB a* = " + str(round(cielab_a_all_mean, 2)) + ", b* = " + str(round(cielab_b_all_mean, 2)) + "."
