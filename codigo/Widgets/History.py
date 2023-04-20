import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import abspath, dirname, join
from user_data.User import Usuario

# from api_reddit import make_posts_reddit


class History:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")

    def destroy(self):
        self.starMap.destroy()
    
    
    def __init__(self, master: tk.Tk, user: Usuario) -> None:

        self.user = user

        self.starMap = tk.Frame(master, width= 764, height= 750, background= "black", highlightthickness=0)
        self.starMap.update_idletasks()
        # self.starMap.place(x= posx, y= posy)
        self.starMap.grid(sticky="nsew")

        scrollbar = ttk.Scrollbar(master=self.starMap, orient="horizontal")
        scrollbar.grid(row=1, column=0, sticky="EW")

        ###
        self.canvasPosition = tk.Canvas(self.starMap, highlightthickness=0, background= "black", xscrollcommand= scrollbar.set, width=764)
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        scrollbar.config(command=self.canvasPosition.xview)

        self.map_history = list(user.historial)
        self.reddit_history = list(user.historial_reddit)

        self.info_container = tk.Frame(master = self.canvasPosition, background="black", width=764)
        self.info_container.grid(row=0, column=0, sticky="nsew")

        self.info_container.bind("<Configure>", lambda e: self.canvasPosition.configure(scrollregion=self.canvasPosition.bbox("all")))
        self.window = self.canvasPosition.create_window((0, 0), window=self.info_container, anchor="nw")

        self.objectNameText = tk.Label(self.info_container, text= "Maps", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectNameText.grid(row = 0, column = 0)

        self.objectIdText = tk.Label(self.info_container, text= "Publications", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectIdText.grid(row = 0, column = 1)

        for i in range(len(self.map_history)):

            print(self.map_history[i])

            history_line = tk.Label(master=self.info_container, 
                                    text= " ".join(self.map_history[i]),
                                    background="black",
                                    fg="white",
                                    height=2, width=50)
            
            history_line.grid(row=(2*i)+1, column=0, sticky="EW")
            history_line.update_idletasks()

        
        for i in range(len(self.reddit_history)):

            print(self.reddit_history[i][1])

            history_line = tk.Label(master=self.info_container, 
                                    text= "".join(self.reddit_history[i][1]),
                                    background="black",
                                    fg="white",
                                    height=2,
                                    justify="left")

            history_line.grid(row=(2*i)+1, column=1, sticky="EW")
            history_line.update_idletasks()

        
        

        
        