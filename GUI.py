from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from matchableImage import MatchableImage
from helperFunctions import getFacialLandmarks
from PIL import Image, ImageTk

from task_FacialLandmarks import plotFacialLandmarks
from task_Expression import checkExpression
from task_Glasses import checkGlasses

from task_Background import checkBackground
from task_Dynamicrange import checkDynamicRange
from task_Contrast import checkContrast

from task_Geometry import checkGeometry
from task_Lighting import checkLighting
from task_Contrast import checkContrast

import os
import cv2
import dlib
import numpy as np

Check_Cut=False
plot_landmarks=False

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class myUI(Frame, metaclass=Singleton):

    def __init__(self):
        Frame.__init__(self)
        #variables
        Check_Cut = IntVar()
        plot_landmarks = IntVar()

        self.filepath_label = StringVar()
        self.filename_label = StringVar()
        self.score_label = StringVar()
        self.type_label = StringVar()
        self.filenumber_label = StringVar()
        self.filepath = ""
        self.file_list = []
        self.currentDisplayedResult = 1
        self.typeLabelList = []
        self.scoreLabelList = []
        self.checkindex_label= StringVar()

        self.expression_type_label = StringVar()
        self.glasses_type_label = StringVar()
        self.color_type_label = StringVar()
        self.lighting_type_label = StringVar()
        self.contrast_type_label = StringVar()
        self.background_type_label = StringVar()
        self.dynamicrange_type_label = StringVar()
        self.contrast_type_label = StringVar()
        self.geometry_type_label = StringVar()
        self.expression_score_label = StringVar()
        self.glasses_score_label = StringVar()
        self.color_score_label = StringVar()
        self.lighting_score_label = StringVar()
        self.background_score_label = StringVar()
        self.contrast_score_label = StringVar()
        self.dynamicrange_score_label = StringVar()
        self.contrast_score_label = StringVar()
        self.geometry_score_label = StringVar()

        #define Window properties
        self.master.title("ICAOcheck")
        self.master.minsize(width=800, height=490)
        self.grid_rowconfigure(0, minsize = 10)
        self.grid_rowconfigure(2, minsize = 10)
        self.grid_rowconfigure(4, minsize = 10)
        self.grid_rowconfigure(6, minsize = 10)
        self.grid_columnconfigure(0, minsize = 10)
        self.grid(sticky=W+E+N+S)

        #define Window objects
        self.filepathLabel = Label(self, textvariable = self.filepath_label)
        self.filepathLabel.grid(row=1, column=2, sticky=W,columnspan = 10)
        self.browseButton = Button(self, text="Browse", command=self.load_files, width=10)
        self.browseButton.grid(row=1, column=1, sticky=W)
        self.checkButton = Button(self, text="Check", command=self.check_images, width=10)
        self.checkButton.grid(row=3, column=1, sticky=W)
        self.checkBox=Checkbutton(self,text="wenn möglich nach ICAO-Standard zuschneiden", command=self.check_cut)
        self.checkBox.grid(row=3, column=2,columnspan=3, sticky=W)
        self.checkBox=Checkbutton(self,text="Facial Landmarks der Bilder anzeigen", command=self.plot_landmarks)
        self.checkBox.grid(row=3, column=6,columnspan=3, sticky=W)

    def check_cut (self):
        global Check_Cut
        Check_Cut= not Check_Cut

    def plot_landmarks(self):
        global plot_landmarks
        plot_landmarks = not plot_landmarks

    def load_files(self):
        #load all files in the same directory as the selected file
        self.filepath = askopenfilename(initialdir = "C:/",title = "Load an Image file",filetypes = (("Image files","*.jpg;*.png;*.bmp;*.tif"),("All files","*.*")))
        dirpath = self.filepath.rsplit('/',1)[0]+'/'
        self.filepath_label.set(dirpath)

        #initialize file list
        self.file_list = []

        #add files to filelist
        for filename in os.listdir(dirpath):
            if ".jpg" in filename or ".png" in filename or ".tif "in filename or ".bmp" in filename or ".jpeg" in filename:
                self.file_list.append(MatchableImage(dirpath, filename))

        if (len(self.file_list) > 0):
            self.display_result(self.file_list[0])

    def check_images(self):
        global Check_Cut
        global plot_landmarks

        if(self.file_list != []):
            detector = dlib.get_frontal_face_detector()
            #load dlib pre-trained predictor
            predictor = dlib.shape_predictor(os.path.realpath(__file__).replace('\\', '/').rsplit('/',1)[0]+'/'+"shape_predictor_68_face_landmarks.dat")
            
            for image in self.file_list:
                #run helper function to set the facial landmark array for each image and set a flag whether the number of faces != 1
                (image.facial_landmarks, image.facial_landmarks_error) = getFacialLandmarks(image,detector,predictor)
                
        #    checkExpression(self.file_list)
        #    checkGlasses(self.file_list)
        #    checkLighting(self.file_list)  #also includes color check
        #    checkBackground(self.file_list)
        #    checkDynamicRange(self.file_list)
        #    checkContrast(self.file_list)
        #    checkGeometry(self.file_list,Check_Cut)
        #    if plot_landmarks==1:
        #        plotFacialLandmarks(self.file_list)

            self.display_result(self.file_list[self.currentDisplayedResult-1])
        #ToDo


    def switchDisplayedImage(self, imageOffset):
        if ((self.currentDisplayedResult + imageOffset) <= len(self.file_list)) and ((self.currentDisplayedResult + imageOffset) >= 1):
            self.currentDisplayedResult += imageOffset
            self.display_result(self.file_list[self.currentDisplayedResult-1])

    def display_result(self, matchableImg):
        #generate Image from filepath
        image = Image.open(matchableImg.image_path+matchableImg.image_name)
        image.thumbnail((280, 360), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.imageWindow = Canvas(self, width = 280, height = 360)
        self.imageWindow.create_image(0,0, anchor = NW, image = photo)
        self.imageWindow.image = photo
        self.imageWindow.grid(row = 7, column = 1, rowspan = 9, columnspan = 2, sticky=W+N)

        #display matching results for currently displayed image
        #self.scoreLabel = Label(self, textvariable = self.score_label)
        #self.scoreLabel.grid(row = 7, column = 6, sticky = E+N)

        #draw label that shows the image-number we are currently seeing
        self.pageLabel = Label(self, textvariable = self.filenumber_label)
        self.pageLabel.grid(row=6, column=1, sticky=N)
        self.filenumber_label.set(str(self.currentDisplayedResult)+" / "+str(len(self.file_list)))

        #draw Button for iteration back through the images
        if self.currentDisplayedResult > 1:
            self.back = Button(self, text="<", command = lambda: self.switchDisplayedImage(-1))
            self.back.grid(row=6, column=1, sticky=W)

        #draw Button for iteration forward through the images
        if self.currentDisplayedResult < len(self.file_list):
            self.forth = Button(self, text=">", command = lambda: self.switchDisplayedImage(1))
            self.forth.grid(row=6, column=1, sticky=E)

        #draw label that shows the image-name we are currently seeing
        self.nameLabel = Label(self, textvariable = self.filename_label)
        self.nameLabel.grid(row=6, column=2,columnspan=3, sticky=W)
        self.filename_label.set("  "+str(self.file_list[self.currentDisplayedResult-1].image_name))

        if (len(self.file_list) > 0):
            #type

            #Patrick
            self.expressiontypeLabel= Label(self, textvariable = self.expression_type_label)
            self.expressiontypeLabel.grid(row = 7, column = 4, sticky = W)
            self.expression_type_label.set(str("Expression:"))

            self.glassestypeLabel= Label(self, textvariable = self.glasses_type_label)
            self.glassestypeLabel.grid(row = 8, column = 4, sticky = W)
            self.glasses_type_label.set(str("Glasses:"))

            #Tobias
            self.colortypeLabel= Label(self, textvariable = self.color_type_label)
            self.colortypeLabel.grid(row = 9, column = 4, sticky = W)
            self.color_type_label.set(str("Color:"))

            self.lightingtypeLabel= Label(self, textvariable = self.lighting_type_label)
            self.lightingtypeLabel.grid(row = 10, column = 4, sticky = W)
            self.lighting_type_label.set(str("Lighting:"))

            #Tim
            self.backgroundtypeLabel= Label(self, textvariable = self.background_type_label)
            self.backgroundtypeLabel.grid(row = 11, column = 4, sticky = W)
            self.background_type_label.set(str("Background:"))

            self.dynamicrangetypeLabel= Label(self, textvariable = self.dynamicrange_type_label)
            self.dynamicrangetypeLabel.grid(row = 12, column = 4, sticky = W)
            self.dynamicrange_type_label.set(str("Dynamic Range:"))

            self.contrasttypeLabel= Label(self, textvariable = self.contrast_type_label)
            self.contrasttypeLabel.grid(row = 13, column = 4, sticky = W)
            self.contrast_type_label.set(str("Contrast:"))

            #Tom
            self.geometrytypeLabel= Label(self, textvariable = self.geometry_type_label)
            self.geometrytypeLabel.grid(row = 14, column = 4, sticky = W)
            self.geometry_type_label.set(str("Geometry:"))

            #score
            #Patrick
            self.expressionscoreLabel= Label(self, textvariable = self.expression_score_label, justify=LEFT)
            self.expressionscoreLabel.grid(row = 7, column = 6, sticky = W)
            self.expression_score_label.set(str(matchableImg.matching_results["Expression"]))

            self.glassesscoreLabel= Label(self, textvariable = self.glasses_score_label, justify=LEFT)
            self.glassesscoreLabel.grid(row = 8, column = 6, sticky = W)
            self.glasses_score_label.set(str(matchableImg.matching_results["Glasses"]))

            #Tobias
            self.colorscoreLabel= Label(self, textvariable = self.color_score_label, justify=LEFT)
            self.colorscoreLabel.grid(row = 9, column = 6, sticky = W)
            self.color_score_label.set(str(matchableImg.matching_results["Color"]))

            self.lightingscoreLabel= Label(self, textvariable = self.lighting_score_label, justify=LEFT)
            self.lightingscoreLabel.grid(row = 10, column = 6, sticky = W)
            self.lighting_score_label.set(str(matchableImg.matching_results["Lighting"]))

            #Tim
            self.backgroundscoreLabel= Label(self, textvariable = self.background_score_label, justify=LEFT)
            self.backgroundscoreLabel.grid(row = 11, column = 6, sticky = W)
            self.background_score_label.set(str(matchableImg.matching_results["Background"]))

            self.dynamicrangeLabel= Label(self, textvariable = self.dynamicrange_score_label, justify=LEFT)
            self.dynamicrangeLabel.grid(row = 12, column = 6, sticky = W)
            self.dynamicrange_score_label.set(str(matchableImg.matching_results["Dynamic Range"]))

            self.contrastLabel= Label(self, textvariable = self.contrast_score_label, justify=LEFT)
            self.contrastLabel.grid(row = 13, column = 6, sticky = W)
            self.contrast_score_label.set(str(matchableImg.matching_results["Contrast"]))

            #Tom
            self.geometryscoreLabel= Label(self, textvariable = self.geometry_score_label, justify=LEFT)
            self.geometryscoreLabel.grid(row = 14, column = 6, sticky = W )
            self.geometry_score_label.set(str(matchableImg.matching_results["Geometry"]))

        self.update()
