import cv2

class MatchableImage:
    #initialize new matchableImage class to contain image data of each image
    def __init__(self, path, filename):
        self.image_name = filename
        self.image_path = path
        #contains 68 facial landmarks
        #facial_landmarks[n][m]: n is the facial landmark from 0 to 67, m is the pixel-coordinate of landmark n (0 = x-value, 1 = y-value)
        self.facial_landmarks = None
        self.facial_landmarks_error = False

        self.matching_results= {"Expression": "", "Glasses": "", "Color": "" , "Lighting": "", "Background": "" , "Geometry": "", "Dynamic Range": "", "Contrast": ""}
