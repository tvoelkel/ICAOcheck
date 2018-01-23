import dlib
import cv2
import os
from datetime import datetime

def plotFacialLandmarks(imagelist):
    #get the current day and time
    now= datetime.now()
    #format the datetime values in a string
    _now='%s.%s.%s_%s-%s-%s' % (now.day, now.month, now.year, now.hour, now.minute, now.second)
    #path where the pictures will be saved (create a new folder)
    result_path=imagelist[0].image_path[:-1]+"-FacialLandmarks"+str(_now)
    os.mkdir(result_path)

    for image in imagelist:
        #get the image data
        image_data = cv2.imread(image.image_path + image.image_name)
        #get the landmarks
        shape = image.facial_landmarks

        #set all 69 landmarks
        for i in range(0,68):

            #get every facial landmark
            point =  (int(shape[i][0]), int(shape[i][1]))
            #set the landmark on this point with rad
            cv2.circle(image_data,(point[0],point[1]), 4, (0,0,255), -1)

        #show every image with facial landmarks

        # cv2.namedWindow("Facial landmarks in picture", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
        # imS = cv2.resize(image_data, (1200, 800))                    # Resize image
        # cv2.imshow("Facial landmarks in picture", imS)                            # Show image
        # cv2.waitKey(0)
        # cv2.resizeWindow(image_data, 600, 600)
        # cv2.imshow("Facial landmarks in picture", image_data)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #save the image in the folder
        cv2.imwrite(result_path+"\\" + image.image_name[:-4]+"-facial_landmarks.jpg", image_data)
