import cv2

class MatchableImage:
    #initialize new matchableImage class to contain image data of each image
    def __init__(self, path, filename):
        self.image_name = filename
        self.image_path = path

        #initialize a list to contain whether an Image is rule-conform or not
        #initialize a list to contain all matching scores
        self.matching_result = []
        self.matching_score_list = []