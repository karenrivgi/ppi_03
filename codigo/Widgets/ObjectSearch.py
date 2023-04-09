import datetime
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import filedialog
from os.path import abspath, dirname, join
# from api_reddit import make_posts_reddit


class ObjectSearch:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")

    def do_nothing():
        pass

    def __init__(self, master: tk.Tk, user = None) -> None:

        self.user = user

        self.starMap = tk.Canvas(master, width= 764, height= 750, background= "black", highlightthickness=0)
        self.starMap.update_idletasks()
        # self.starMap.place(x= posx, y= posy)
        self.starMap.grid(sticky="nsew")

        ###
        self.canvasPosition = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        self.objectNameText = tk.Label(self.canvasPosition, text= "Object Name", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectNameText.grid(row = 0, column = 0)

        self.objectIdText = tk.Label(self.canvasPosition, text= "Object ID", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectIdText.grid(row = 0, column = 1)
        
        self.objectName = tk.Entry(
            master=self.canvasPosition,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.objectName.grid(row = 1, column = 0, padx = 5, pady = 5)

        self.objectId = tk.Entry(
            master=self.canvasPosition,
            bd = 0,
            highlightthickness = 0,
            font=("BeVietnamPro 12"), width = 15)
        
        self.objectId.grid(row = 1, column = 1, padx = 5, pady = 5)

    
        ###
        self.buttonParent = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.buttonParent.update_idletasks()
        self.buttonParent.grid(row=1, column=0, sticky="nsew")
        self.buttonParent.grid_anchor("center")

        self.img0 = tk.PhotoImage(file = join(ObjectSearch.recursos_path,"SubmitButton.png"))
        self.submitButton = tk.Button(
            master= self.buttonParent,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.do_nothing,
            relief = "flat",
            state="disabled",
            bg= "black")
        
        self.submitButton.grid(row=0, column=1, columnspan=2, padx = 5, pady = 5)

        self.img1 = tk.PhotoImage(file = join(ObjectSearch.recursos_path,"SaveButon.png"))
        self.saveButton = tk.Button(
            master= self.buttonParent,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.do_nothing,
            relief = "flat",
            bg= "black")
        
        self.saveButton.grid(row=0, column=0, padx = 5, pady = 5)
           
        self.figMaster = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.figMaster.update_idletasks()
        self.figMaster.grid(row=3, column = 0, sticky="nsew")
        self.figMaster.grid_anchor("s")
        self.figMaster.update_idletasks()
        #print(self.figMaster.winfo_height())

        self.canvasStarsInfo = tk.Canvas(self.starMap, width= 220, highlightthickness=0, background= "black")
        self.figMaster.update_idletasks()
        self.canvasStarsInfo.grid(row = 0, column = 1, rowspan=4, sticky="ns")
