import tkinter as tk
from tkinter import ttk
from os.path import abspath, dirname, join
from Widgets.Helpers import WebScrapping
from tkhtmlview import HTMLLabel

class MapInfo:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")

    def do_nothing():
        pass

    def destroy(self):
        self.starMap.destroy()

    def __init__(self, master: tk.Tk, estrellas=None, planeta = None,
                  constelacion = None, user = None) -> None:

        self.user = user

        self.starMap = tk.Frame(master, width= 764, height= 750, background= "black", highlightthickness=0)
        self.starMap.update_idletasks()
        self.starMap.pack(expand=True)

        # Crea un scrollbar vertical y lo posiciona, para visualizar todo el contenido
        scrollbar = ttk.Scrollbar(master=self.starMap, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        canvas = tk.Canvas(master=self.starMap, yscrollcommand=scrollbar.set, width= 745, height= 750, background="black")
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)  

        self.inner_frame = tk.Frame(canvas, background="black")
        canvas.create_window((0,0), window=self.inner_frame, anchor="nw", width=745)

        mapinfo = WebScrapping.map_info(constelacion, estrellas, planeta)
        
        for key in mapinfo.keys():

            if key == 'Stars':

                for star in mapinfo[key]:
                    my_label = HTMLLabel(self.inner_frame, html=star)

                    # Adjust label
                    my_label.pack(pady=3,fill="both", expand=True)


            else:
                my_label = HTMLLabel(self.inner_frame, html=mapinfo[key])

                # Adjust label
                my_label.pack(pady=3, fill="both", expand=True)

        self.inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
