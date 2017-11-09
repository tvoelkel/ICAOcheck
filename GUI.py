from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class myUI(Frame, metaclass=Singleton):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("ICAOcheck")
        self.master.minsize(width=666, height=666)
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)
        self.filepath = StringVar()

        self.label = Label(self, textvariable = self.filepath)
        self.label.grid(row=0, column=1, sticky=W)
        self.button = Button(self, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=0, column=0, sticky=W)

    def load_file(self):
        self.filepath.set(askopenfilename(initialdir = "C:/",title = "Load an Image file",filetypes = (("image files","*.jpg;*.png;*.bmp;*.tif"),("all files","*.*"))))

    def get_filepath(self):
        return self.filepath
