import tkinter as tk
from tkinter import ttk
from os.path import abspath, dirname, join
from user_data.User import Usuario


class MyAstros:

    recursos_path = join(dirname(dirname(abspath(__file__))),"Recursos")
    
    def __init__(self, master: tk.Tk, user: Usuario) -> None:

        self.user = user

        # Obtenemos la información de los historiales del usuario
        self.historial_astros = list(user.historial_astros)

        # Creacion del contenedor de los objetos de la ventana.
        self.myAstros = tk.Frame(master, background="black", highlightthickness=0)
        self.myAstros.pack(fill='both', expand=True)

        # Crea un scrollbar vertical y lo posiciona, para visualizar todo el contenido
        scrollbarV = ttk.Scrollbar(master=self.myAstros, orient="vertical")
        scrollbarV.pack(side="right", fill='y')

        # Crea la tabla para contener la información del historial
        self.treeAstros = ttk.Treeview(self.myAstros, yscrollcommand=scrollbarV.set)
        self.treeAstros.pack(fill="both", expand=True)

        # Configura el scrollbar vertical para modificar el eje y de la tabla
        scrollbarV.config(command=self.treeAstros.yview)
        
        self.astros_table()

    def astros_table(self):
        
        # Se le da estilo al Tree
        styletable = ttk.Style()

        styletable.theme_use("clam")

        styletable.configure(
            "Treeview",
            background="LigthSteelBlue3",
            foreground="black",
            rowheigth=50,
            fieldbackground="light cyan"
                             )
        
        # Columnas del Tree
        self.treeAstros["columns"] = ("Planets", "Stars")

        # Le damos formato a las columnas
        self.treeAstros.column("#0", width=0, stretch=False) # columna por defecto
        self.treeAstros.column("Planets", width=375)
        self.treeAstros.column("Stars", width=375)

        # creamos los headings de las columnas
        self.treeAstros.heading("#0", text="", anchor="w") # columna por defecto
        self.treeAstros.heading("Planets", text="Planets", anchor="center")
        self.treeAstros.heading("Stars", text="Stars", anchor="center")

        # Listas para diferenciar por typo de astro y almacenarlos
        listaplanetas=[]
        listaestrella=[] 

        #For para filtrar por tipo de dato y almacenar  
        for astro in range(len(self.historial_astros)):
            if self.historial_astros[astro][0] == 'planet':
                listaplanetas.append(self.historial_astros[astro][1])
            else:
                listaestrella.append(self.historial_astros[astro][1])

        #If para agregar los astros a la columna que pertenezca
        if len(listaestrella)>=len(listaplanetas):
            Contador1=len(listaestrella)
            while Contador1>=1:
                if len(listaplanetas)>0:
                    self.treeAstros.insert(parent="" ,index="end" ,text="", values=(listaplanetas[0],listaestrella[0]))
                    listaplanetas.pop(0)
                    listaestrella.pop(0)        
                elif len(listaestrella)>0:
                    self.treeAstros.insert(parent="" ,index="end" ,text="", values=(" ",listaestrella[0]))
                    listaestrella.pop(0) 
                else:
                    break
        else:
            Contador2=len(listaplanetas)
            while Contador2>=1:
                if len(listaestrella)>0:
                    self.treeAstros.insert(parent="" ,index="end" ,text="", values=(listaplanetas[0],listaestrella[0]))
                    listaplanetas.pop(0)
                    listaestrella.pop(0)
                elif len(listaplanetas)>0: 
                    self.treeAstros.insert(parent="" ,index="end" ,text="", values=(listaplanetas[0]," "))
                    listaplanetas.pop(0)
                else:
                    break


    def destroy(self):
        """Destruye el widget del objeto tkinter."""
        self.history.destroy()
