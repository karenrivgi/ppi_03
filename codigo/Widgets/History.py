import datetime
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import abspath, dirname, join
# from api_reddit import make_posts_reddit


class History:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")

    def destroy(self):
        self.starMap.destroy()
    
    
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

        self.objectNameText = tk.Label(self.canvasPosition, text= "Maps", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectNameText.grid(row = 0, column = 0)

        self.objectIdText = tk.Label(self.canvasPosition, text= "Publications", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectIdText.grid(row = 0, column = 1)
        
        