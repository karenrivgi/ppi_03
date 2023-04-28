import tkinter as tk
from tkinter import ttk
from os.path import abspath, dirname, join
from user_data.User import Usuario
from Widgets.ObjectSearch import ObjectSearch
import webbrowser


class MyAstros:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")
    
    def __init__(self, master: tk.Tk, user: Usuario) -> None:

        self.user = user

        # Creacion del contenedor de los objetos de la ventana.
        self.history = tk.Frame(master, width=748, height=731, background="black", highlightthickness=0)
        self.history.grid(sticky="nsew")

        # Crea un scrollbar vertical y lo posiciona, para visualizar todo el contenido
        scrollbarv = ttk.Scrollbar(master=self.history, orient="vertical")
        scrollbarv.grid(row=0, column=1, sticky='ns')

        # Creación del canvas auxiliar para el funcionamiento del scrollbar
        self.canvasPosition = tk.Canvas(self.history, highlightthickness=0, background="black", yscrollcommand=scrollbarv.set, width=748, height=731)
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        # Crea un frame para contener la información del historial
        self.info_container = tk.Frame(master=self.canvasPosition, background="black", width=748, height=731)
        self.canvasPosition.create_window((0, 0), window=self.info_container, anchor="nw")

        # Configura el scrollbar vertical para modificar el eje y del canvas
        scrollbarv.config(command=self.canvasPosition.yview)

        # Configuramos el frame para que se actualice en base a la posición del scrollbar
        self.info_container.bind("<Configure>", lambda e: self.canvasPosition.configure(scrollregion=self.canvasPosition.bbox("all")))


        # Creamos los títulos y los posicionamos en info_container
        self.objectNameText = tk.Label(self.info_container, text= "Favorite Astros", font = ("BeVietnamPro-Bold", int(12)), width = 15, fg = "#ffffff", bg= "black")
        self.objectNameText.grid(row = 0, column = 0)

        # Obtenemos la información de los historiales del usuario
        self.historial_astros = list(user.historial)

        for i in range(len(self.historial_astros)):
            # Crea un label para el elemento actual del historial
            history_line = tk.Label(master=self.info_container, 
                                    text= " ".join(self.historial_astros[i]),
                                    background="black",
                                    fg="white",
                                    height=2, width=50)
            
            # Lo posiciona en info_container con grid
            history_line.grid(row=(2*i)+1, column=0, sticky="EW")
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
