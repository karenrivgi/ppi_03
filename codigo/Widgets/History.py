import tkinter as tk
import webbrowser

from tkinter import ttk
from os.path import abspath, dirname, join
from user_data.User import Usuario

class History:
    
    def __init__(self, master: tk.Tk, user: Usuario) -> None:

        self.user = user
        master.pack_propagate(False)

        # Creacion del contenedor de los objetos de la ventana.
        self.history = tk.Frame(master, background="black", highlightthickness=0)
        self.history.pack(fill="both", expand=True)

        # Crea un scrollbar horizontal y lo posiciona, para visualizar todo el contenido
        scrollbar = ttk.Scrollbar(master=self.history, orient="horizontal")
        scrollbar.pack(side="bottom", fill="x")

        # Crea un scrollbar vertical y lo posiciona, para visualizar todo el contenido
        scrollbarv = ttk.Scrollbar(master=self.history, orient="vertical")
        scrollbarv.pack(side="right", fill="y")

        # Crea la tabla para contener la información del historial
        self.tree = ttk.Treeview(self.history, yscrollcommand=scrollbarv.set, xscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=True)

        # Configura el scrollbar horizontal para modificar el eje x de la tabla
        scrollbar.config(command=self.tree.xview)

        # Configura el scrollbar vertical para modificar el eje y de la tabla
        scrollbarv.config(command=self.tree.yview)

        # funcion para llenar la tabla y ponerle los estilos
        self.populate_treeview()

        # event listener para cuando se le dé doble click, abrir el link de reddit si es posible
        self.tree.bind("<Double-1>", self.selected_entry)

    def populate_treeview(self):
        """funcion encargada de fdarle estilo a la tabla, y de insertar los datos del historial del usuario"""

        # para agregarle estilos al tree
        style = ttk.Style()
        style.configure("Treeview", 
                        background="SkyBlue1",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="lightblue",
                        )
        style.map("Treeview",
                  background=[("selected", "blue")])

        # Definimos las columnas con las que vamos a trabajar
        self.tree["columns"] = ("Date", "Map", "Reddit post")

        # Le damos formato a las columnas
        self.tree.column("#0", width=0, stretch=False) # columna por defecto
        self.tree.column("Date", width=250)
        self.tree.column("Map", width=250)
        self.tree.column("Reddit post", width=250)

        # creamos los headings de las columnas
        self.tree.heading("#0", text="", anchor="w") # columna por defecto
        self.tree.heading("Date", text="Date", anchor="center")
        self.tree.heading("Map", text="Map", anchor="center")
        self.tree.heading("Reddit post", text="Reddit post", anchor="center")

        # creamos tags para mostrar adecuadamente las filas segun su posicion
        self.tree.tag_configure("impar", background="lightblue")
        self.tree.tag_configure("par", background="#2255a5")

        # insertamos los datos
        try:
            id = 0
            for entry in self.user.historial:
                tag = ("par",) if id % 2 == 0 else ("impar",)

                if isinstance(entry[3], list):
                    self.tree.insert(parent="", index="end", iid=id, text="", values=(entry[0], " - ".join((entry[1], entry[2])), entry[3][1]), tags=tag)
                else:
                    self.tree.insert(parent="", index="end", iid=id, text="", values=(entry[0], " - ".join((entry[1], entry[2])), entry[3]), tags=tag)

                id += 1
        
        except:
            pass
    
    def open_url(self,url):
        """función que abrirá la URL especificada en el navegador web"""
        
        # Abre la url especificada en el navegador web
        webbrowser.open_new(url)
        
    def selected_entry(self, ev):
        """funcion encargada de comprobar si hay un link asociado a la publicacion en el historial
        para posteriormente llamar la funcion que se encarga de abrir el navegador"""

        selected = self.tree.focus()
        url = self.tree.item(selected, "values")[2]

        if url != "Not published":
            self.open_url(url)
            
    def destroy(self):
        """Destruye el widget del objeto tkinter."""
        self.history.destroy()

        
        