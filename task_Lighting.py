import numpy as np
import dlib
import cv2
import os

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
        return "Error: More than one face detected."
    elif len(face_rectangle_array) == 0:
        return "Error: No face detected."
    else:
        shape = shapeToArray(predictor(img, face_rectangle_array[0]))
        return computeImage(image, shape)

def getPredictorFilepath(predictorFilename):
    #for this to work, the facial landmark predictor has to be located inside the same folder as "task_Lightning.py"
    return os.path.realpath(__file__).replace('\\', '/').rsplit('/',1)[0]+'/'+predictorFilename

def computeImage(image, shape):
    return shape[1][0]

def shapeToArray(shape):
    #convert dlib shape object to array
    array = np.zeros((68,2), dtype=np.int)

    #iterate over the facial landmarks
    for i in range(0, 68):
        array[i] = (shape.part(i).x, shape.part(i).y)

    return array
