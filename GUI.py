from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from matchableImage import MatchableImage

import os
import cv2

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
        self.filepath_label = StringVar()
        self.filepath = ""
        self.file_list = []

        #define Window properties
        self.master.title("ICAOcheck")
        self.master.minsize(width=666, height=666)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        #define Window objects
        self.label = Label(self, textvariable = self.filepath_label)
        self.label.grid(row=0, column=1, sticky=W)
        self.button = Button(self, text="Browse", command=self.load_files, width=10)
        self.button.grid(row=0, column=0, sticky=W)

    def load_files(self):
        #load all files in the same directory as the selected file
        self.filepath = askopenfilename(initialdir = "C:/",title = "Load an Image file",filetypes = (("Image files","*.jpg;*.png;*.bmp;*.tif"),("All files","*.*")))
        dirpath = self.filepath.rsplit('/',1)[0]+'/'
        self.filepath_label.set(dirpath)

        #add files to filelist
        for filename in os.listdir(dirpath):
            self.file_list.append(MatchableImage(dirpath, filename))
