from PIL import Image
import cv2
#from matplotlib import pyplot as plt

def checkDynamicRange(imagelist):
    
    for image in imagelist:
        image_data = cv2.imread(image.image_path + image.image_name,0)
        """color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([image_data],[i])
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.show()
        """
        image.matching_results["Dynamic Range"]= image_data