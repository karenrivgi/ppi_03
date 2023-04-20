import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from os.path import abspath, dirname, join
from user_data.User import Usuario
import webbrowser


class History:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")
    
    def __init__(self, master: tk.Tk, user: Usuario) -> None:

        self.user = user

        # Creacion del contenedor de los objetos de la ventana.
        self.history = tk.Frame(master, width= 764, height= 750, background= "black", highlightthickness=0)
        self.history.update_idletasks()
        self.history.grid(sticky="nsew")

        # Crea un scrollbar horizontal y lo posiciona, para visualizar todo el contenido
        scrollbar = ttk.Scrollbar(master=self.history, orient="horizontal")
        scrollbar.grid(row=1, column=0, sticky="EW")

        # Creación del canvas auxiliar para el funcionamiento del scrollbar
        self.canvasPosition = tk.Canvas(self.history, highlightthickness=0, background= "black", xscrollcommand= scrollbar.set, width=764)
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")
        
        # Configura el scrollbar para modificar en el eje x
        scrollbar.config(command=self.canvasPosition.xview)

        # Crea un frame para contener la información del historial
        self.info_container = tk.Frame(master = self.canvasPosition, background="black", width=764)
        self.info_container.grid(row=0, column=0, sticky="nsew")

        # Configuramos el frame para que se actualice en base a la posición del scrollbar
        self.info_container.bind("<Configure>", lambda e: self.canvasPosition.configure(scrollregion=self.canvasPosition.bbox("all")))
        self.window = self.canvasPosition.create_window((0, 0), window=self.info_container, anchor="nw")

        # Creamos los títulos y los posicionamos en info_container
        self.objectNameText = tk.Label(self.info_container, text= "Maps", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectNameText.grid(row = 0, column = 0)
        self.objectIdText = tk.Label(self.info_container, text= "Publications", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectIdText.grid(row = 0, column = 1)

        # Obtenemos la información de los historiales del usuario
        self.map_history = list(user.historial)
        self.reddit_history = list(user.historial_reddit)

        for i in range(len(self.map_history)):
            # Crea un label para el elemento actual del historial
            history_line = tk.Label(master=self.info_container, 
                                    text= " ".join(self.map_history[i]),
                                    background="black",
                                    fg="white",
                                    height=2, width=50)
            
            # Lo posiciona en info_container con grid
            history_line.grid(row=(2*i)+1, column=0, sticky="EW")
            history_line.update_idletasks()

        
        for i in range(len(self.reddit_history)):
            # Crea un label para el elemento actual del historial, que es una url
            url = "".join(self.reddit_history[i][1])
            history_line = tk.Label(master=self.info_container, 
                                    text= url,
                                    background="black",
                                    fg="white",
                                    height=2,
                                    justify="left")
            
            # Configurar el Label como hipervínculo
            history_line.config(fg="blue", cursor="hand2")
            history_line.bind("<Button-1>", self.open_link(url))

            # Lo posiciona en info_container con grid
            history_line.grid(row=(2*i)+1, column=1, sticky="EW")
            history_line.update_idletasks()

    
    def open_link(self, url):
        """ Devuelve una función que abrirá la URL especificada en el navegador web
        cuando se ejecute como un controlador de eventos para un widget tkinter. """

        def open_url(event):
            # Abre la url especificada en el navegador web
            webbrowser.open_new(url)
        return open_url
        
    
    def destroy(self):
        """Destruye el widget del objeto tkinter."""
        self.history.destroy()

        
        