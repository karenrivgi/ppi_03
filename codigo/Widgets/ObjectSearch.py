import datetime
import tkinter as tk
import polars as pl
import os
import matplotlib.pyplot as plt
import Widgets.Helpers.WebScrapping as ws
from tkhtmlview import HTMLLabel
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from tkinter import filedialog
from os.path import abspath, dirname, join

# from api_reddit import make_posts_reddit


class ObjectSearch:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")
    names_path =  join(dirname(dirname(abspath(__file__))),"StarMapGenerator")

    def show_info(self):

        info = ws.object_search(self.varObjectType.get().lower(), self.varObjectName.get().capitalize())
        label = HTMLLabel(self.figMaster, html= info)
        label.grid(row=0, column=0, sticky="nsew")

        

    def destroy(self):
        self.starMap.destroy()
    
    def planet_star_filter(self, data: pl.DataFrame, op_filter: str):
        
        options = None

        if op_filter == "Star":

            filtered = self.object_dataframe.filter(pl.col("source").str.contains("universeguide"))
            print(filtered)
            options = filtered.get_column("common name").to_list()

        else:
            options = [
                "Mercury", "Venus", "Earth", "Mars",
                "Jupiter", "Saturn", "Uranus", "Neptune"
            ]
            
        self.listaObjectName["menu"].delete(0,'end')
        
        for i in options:
            pass
            self.listaObjectName["menu"].add_command(label=i, command=tk._setit(self.varObjectName, i))
        self.varObjectName.set(options[0])

        self.submitButton.config(state="normal")

    
    def __init__(self, master: tk.Tk, user = None) -> None:

        self.object_dataframe = pl.read_csv(join(ObjectSearch.names_path,"names.csv"), ignore_errors=True)
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
        
        #Lista desplegable que contiene las opciones para Object Type
        self.varObjectType= tk.StringVar(self.canvasPosition)
        self.opcionesObjectType=['Star','Planet']
        self.dicObjectType={'Star':'star','Planet':'planet'}
        self.listaObjectType = tk.OptionMenu(self.canvasPosition,self.varObjectType,*self.opcionesObjectType)
        self.listaObjectType.config(width = 15)
        self.listaObjectType.grid(row = 1, column = 0, padx = 5, pady = 5)


        #Lista desplegable que contiene las opciones para Object Name
        self.varObjectName= tk.StringVar(self.canvasPosition)
        self.listaObjectName = tk.OptionMenu(self.canvasPosition,self.varObjectName, value= [])
        self.listaObjectName.config(width = 15)
        self.listaObjectName.grid(row = 1, column = 1, padx = 5, pady = 5)

    
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
            command = lambda: self.show_info(),
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
            command = lambda: self.planet_star_filter(self.object_dataframe, self.varObjectType.get()),
            relief = "flat",
            bg= "black")
        
        self.saveButton.grid(row=0, column=0, padx = 5, pady = 5)
           
        self.figMaster = tk.Canvas(self.starMap, highlightthickness=0, background= "black")
        self.figMaster.update_idletasks()
        self.figMaster.grid(row=2, column = 0, sticky="nsew")
        self.figMaster.update_idletasks()
