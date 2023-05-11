import datetime
import tkinter as tk
import polars as pl
import Widgets.Helpers.WebScrapping as ws
from tkhtmlview import HTMLLabel
from os.path import abspath, dirname, join


class ObjectSearch:
    """Clase encargada de representar el widget encargado de manejar
    la funcionalidad de busqueda de objetos celestes.

    Atributos:
    - object_dataframe (pl.DataFrame): informacion de los nombres de los
    astros del catalogo hipparcos, disponibles para consultar.
    - user (User): instancia del usuario.
    - canvasPosition (tk.Canvas): canvas contenedor.
    - figMaster (tk.Canvas): canvas contenedor de la informacion.

    Metodos:
    - show_info(): Funcion encargada de agregar la informacion 
    correspondiente del astro seleccionado en pantalla
    - add_favourite(): Funcion encargada de guardar la informacion 
    al añadir un astro en el historial de favoritos.
    - destroy(): Destruye el canvas principal.
    - planet_star_filter(): Funcion encargada de filtrar las 
    opciones de atsros en base a la seleccion del usuario.
    """

    recursos_path = join(dirname(dirname(abspath(__file__))), "Recursos")
    names_path = join(dirname(dirname(abspath(__file__))), "StarMapGenerator")

    def show_info(self):
        """Funcion encargada de agregar la informacion correspondiente
        del astro seleccionado en pantalla, haciendo uso de web scrapping.
        """
        
        for child in self.figMaster.winfo_children():
            child.destroy()

        info = ws.object_search(
            self.varObjectType.get().lower(),
            self.varObjectName.get().capitalize())
        
        label = HTMLLabel(self.figMaster, html=info)
        # label.grid(row=0, column=0, sticky="nsew")
        # label.grid_anchor("center")
        label.pack(expand=True, fill="both")
        self.favouriteButton.config(state="normal")

    def add_favourite(self):
        """Funcion encargada de guardar la informacion al añadir un
        astro en el historial de favoritos.
        """

        time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        astro = [
            self.varObjectType.get().lower(),
            self.varObjectName.get().capitalize(),
            time]

        if astro in self.user.historial_astros:
            pass

        else:
            self.user.guardar_historial(astro, "astros")

        #print(self.user.historial_astros)

    def destroy(self):
        """Destruye el canvas principal"""
        
        self.starMap.destroy()

    def planet_star_filter(self, data: pl.DataFrame, op_filter: str):
        """Funcion encargada de filtrar las opciones de atsros en base
        a la seleccion del usuario

        argumentos:
        - data (pl.DataFrame): datos de los astros del catalogo hipparcos
        - op_filter (str): tipo de astro sobre el que se quiere consultar
        """

        options = None

        if op_filter == "Star":

            filtered = self.object_dataframe.filter(
                pl.col("source").str.contains("universeguide"))
            #print(filtered)
            options = filtered.get_column("common name").to_list()

        else:
            options = [
                "Mercury", "Venus", "Earth", "Mars",
                "Jupiter", "Saturn", "Uranus", "Neptune"
            ]

        self.listaObjectName["menu"].delete(0, 'end')

        for i in options:
            pass
            self.listaObjectName["menu"].add_command(
                label=i, command=tk._setit(self.varObjectName, i))
        self.varObjectName.set(options[0])

        self.submitButton.config(state="normal")

    def __init__(self, master: tk.Canvas, user=None) -> None:
        """Metodo consytructor, encargado de crear toda la estructura
        garfica del widget.

        argumentos:
        - master (tk.Canvas): canvas principal sobre el cual se 
        organiza todo
        - user (User): instancia del usuario usando la app
        """

        # dataframe con los nombres de las estrellas en la base del 
        # catalogo hipparcos
        self.object_dataframe = pl.read_csv(
            join(
                ObjectSearch.names_path,
                "names.csv"),
            ignore_errors=True)
        
        # instancia del usuario
        self.user = user

        # canvas contenedor general
        self.starMap = tk.Canvas(
            master,
            width=764,
            height=750,
            background="black",
            highlightthickness=0)
        self.starMap.update_idletasks()
        self.starMap.place(x=0, y=0)
        # self.starMap.grid(sticky="nsew")

        # canvas contenedor de los diferentes widgets
        self.canvasPosition = tk.Canvas(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        # Label que informa la seccion del tipo de astro
        self.objectNameText = tk.Label(
            self.canvasPosition,
            text="Object Type",
            font=(
                "BeVietnamPro-Bold",
                int(12)),
            width=15,
            fg="#ffffff",
            bg="black")
        self.objectNameText.grid(row=0, column=0)

        # Label que informa la sección de seleccion del astro 
        self.objectIdText = tk.Label(
            self.canvasPosition,
            text="Object Name",
            font=(
                "BeVietnamPro-Bold",
                int(12)),
            width=15,
            fg="#ffffff",
            bg="black")
        self.objectIdText.grid(row=0, column=1)

        # Lista desplegable que contiene las opciones para Object Type
        self.varObjectType = tk.StringVar(self.canvasPosition)
        self.opcionesObjectType = ['Star', 'Planet']
        self.dicObjectType = {'Star': 'star', 'Planet': 'planet'}
        self.listaObjectType = tk.OptionMenu(
            self.canvasPosition,
            self.varObjectType,
            *self.opcionesObjectType)
        self.listaObjectType.config(width=15)
        self.listaObjectType.grid(row=1, column=0, padx=5, pady=5)

        # Lista desplegable que contiene las opciones para Object Name
        self.varObjectName = tk.StringVar(self.canvasPosition)
        self.listaObjectName = tk.OptionMenu(
            self.canvasPosition, self.varObjectName, value=[])
        self.listaObjectName.config(width=15)
        self.listaObjectName.grid(row=1, column=1, padx=5, pady=5)

        # canvas contenedor de los botones
        self.buttonParent = tk.Canvas(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.buttonParent.update_idletasks()
        self.buttonParent.grid(row=1, column=0, sticky="nsew")
        self.buttonParent.grid_anchor("center")

        # boton de guardado
        self.img0 = tk.PhotoImage(
            file=join(
                ObjectSearch.recursos_path,
                "SaveButon.png"))
        self.saveButton = tk.Button(
            master=self.buttonParent,
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.planet_star_filter(
                self.object_dataframe,
                self.varObjectType.get()),
            relief="flat",
            bg="black")

        self.saveButton.grid(row=0, column=0, pady=5)

        # boton para enviar la información
        self.img1 = tk.PhotoImage(
            file=join(
                ObjectSearch.recursos_path,
                "SubmitButton.png"))
        self.submitButton = tk.Button(
            master=self.buttonParent,
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.show_info(),
            relief="flat",
            state="disabled",
            bg="black")
        self.submitButton.grid(row=0, column=1, padx=5, pady=5)

        # boton para agregar un astro al historial de favoritos del usuario
        self.img2 = tk.PhotoImage(
            file=join(
                ObjectSearch.recursos_path,
                "FavouriteButton.png"))
        self.favouriteButton = tk.Button(
            master=self.buttonParent,
            image=self.img2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.add_favourite(),
            relief="flat",
            state="disabled",
            bg="black")
        self.favouriteButton.grid(row=0, column=2, padx=2, pady=5)

        # canvas contenedor de la informacion que se va a extraer
        self.figMaster = tk.Canvas(
            self.starMap,
            highlightthickness=0,
            background="black",
            height=650)
        self.figMaster.grid_propagate(False)
        self.figMaster.pack_propagate(False)
        self.figMaster.grid(row=2, column=0, sticky="nsew")
        self.figMaster.update_idletasks()