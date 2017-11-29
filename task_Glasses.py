import dlib
import cv2

def checkGlasses(imagelist):
    for image in imagelist:
        #image.matching_type_list.append("Expression Check: ")
        #image.matching_score_list.append(image.image_name)

        """
        if checkExistenceOfGlasses == True:
            glasses = True
            if checkEyeVisibility == True:
                eyes_visibility == True
            else:
                eyes_visibility == False
        else:
            glasses == False
        """
        #only for testing
        glasses = False
        eyes_visibility = True
        if glasses == False:
            image.matching_results["Glasses"]="The person does not wear glasses"
        elif glasses == True and eyes_visibility == False:
            image.matching_results["Glasses"]="The person wear glasses, but the eyes are not visible"
        elif glasses == True and eyes_visibility == True:
            image.matching_results["Glasses"]="The person wear glasses and the eyes are visible"

def checkExistenceOfGlasses(image):
    #ToDo check whether the person wear glasses or not
    return False

def checkEyeVisibility(image):
    #ToDo check the visibility of the eyes when the person wear glasses
    return False
