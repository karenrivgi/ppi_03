import datetime
import os
import tkinter as tk
from tkinter import messagebox
from os.path import abspath, dirname, join
from StarMapGenerator import planetHorizon


class ObjectInHorizon:
    """Clase encargada de crear el widget encargado del manejo de la
    funcionalidad de consulta de objeto en el horizonte

    Atributos:
    - horizonCanvas (tk.Canvas): Canvas base encargado de contener los
    demas widgets graficos.

    Metodos:
    - destroy(): Metodo encargado de destruir el canvas base.
    - create_widgets(): Crea los widgets de la interfaz de usuario 
    de la aplicacion, sobre el canvas base.
    - get_times_horizon(): Obtiene los tiempos en que el objeto celeste 
    se eleva y se pone por encima del horizonte para una ubicación y 
    fecha dadas y los muestra por pantalla.
    - save_data(): Guarda los datos pasados por el usuario.
    """

    # Referencia al directorio con los recursos graficos.
    recursos_path = join(dirname(dirname(abspath(__file__))), "Recursos")

    def __init__(self, master: tk.Canvas, user=None):
        """ Constructor de la clase ObjectInHorizon.

        Args:
        - master: objeto Tk raíz para la aplicación.
        - user: parámetro opcional que no se utiliza en esta implementación.
        """
        # Canvas base
        self.horizonCanvas = tk.Canvas(
            master,
            width=764,
            height=732,
            background="black",
            highlightthickness=0)
        self.horizonCanvas.place(
            x=0, y=0, relwidth=1, relheight=1, anchor='nw')

        # Se crean los widgets (labels, campos de entrada, listas y botón).
        self.create_widgets()


    def destroy(self):
        """ Destruye el canvas principal de la aplicación. """
        self.horizonCanvas.destroy()


    def create_widgets(self):
        """ Crea los widgets de la interfaz de usuario de la aplicación. """

        # ---------------------------------------------
        # Frame principal donde se colocarán los widgets.
        self.horizonFrame = tk.Frame(
            self.horizonCanvas,
            width=764,
            height=732,
            background="black",
            highlightthickness=0)
        self.horizonFrame.update_idletasks()

        self.horizonFrame.grid(
            row=0,
            column=0,
            padx=45,
            pady=10,
            sticky="NSEW",
        )

        # Label para el encabezado de la interfaz.
        self.header_label = tk.Label(
            self.horizonFrame,
            text="When is the object above the horizon?",
            font=("BeVietnamPro 30"),
            fg="#ffffff",
            bg="black",
            highlightthickness=0)
        self.header_label.grid(
            row=0,
            column=0,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="WE")

        # -------------------------------------
        # Canvas donde posicionaremos los botones y labels para obtener
        # información sobre la ubicación
        self.canvasPosition = tk.Frame(
            self.horizonFrame,
            highlightthickness=0,
            background="black")
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        # Posicionamos el Label para el país en canvasPosition, usando grid
        self.countryText = tk.Label(
            self.canvasPosition,
            text="Country",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff",
            bg="black")

        self.countryText.grid(row=0, column=0, padx=5, pady=5, sticky="WE")

        # Posicionamos el Label para la providencia en canvasPosition, usando
        # grid
        self.provinceText = tk.Label(
            self.canvasPosition,
            text="Province",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff", bg="black")
        self.provinceText.grid(row=0, column=1, padx=5, pady=5, sticky="WE")

        # Posicionamos el Label para la ciudad en canvasPosition, usando grid
        self.cityText = tk.Label(
            self.canvasPosition,
            text="City",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff",
            bg="black"
        )
        self.cityText.grid(row=0, column=2, padx=5, pady=5, sticky="WE")

        # Creamos un espacio para que el usuario pueda ingresar su país, y lo
        # posicionamos en canvasPosition con Grid
        self.country = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.country.grid(row=1, column=0, padx=5, pady=5, sticky="WE")

        # Creamos un espacio para que el usuario pueda ingresar su providencia,
        # y lo posicionamos en canvasPosition con Grid
        self.province = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.province.grid(row=1, column=1, padx=5, pady=5, sticky="WE")

        # Creamos un espacio para que el usuario pueda ingresar su ciudad, y lo
        # posicionamos en canvasPosition con Grid
        self.city = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.city.grid(row=1, column=2, padx=5, pady=5, sticky="WE")

        # -------------------------------------
        # Canvas donde posicionaremos los botones y labels para obtener
        # información sobre la fecha y hora
        self.canvasDate = tk.Frame(
            self.horizonFrame,
            highlightthickness=0,
            background="black")
        self.canvasDate.update_idletasks()
        self.canvasDate.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.canvasDate.grid_anchor("center")

        # Posicionamos el Label para la fecha en canvasDate, usando grid
        self.dateText = tk.Label(
            self.canvasDate,
            text="Date (AAAA-MM-DD)",
            font=("BeVietnamPro-Bold", int(12)),
            width=18,
            fg="#ffffff",
            bg="black")
        self.dateText.grid(row=0, column=0, padx=5, pady=5, sticky="WE")

        # Posicionamos el Label para la hora en canvasDate, usando grid
        self.objectText = tk.Label(
            self.canvasDate,
            text="Astro",
            font=("BeVietnamPro-Bold", int(12)),
            width=18,
            fg="#ffffff",
            bg="black")
        self.objectText.grid(row=0, column=1, padx=5, pady=5, sticky="WE")

        # Creamos un espacio para que el usuario pueda ingresar una fecha, y lo
        # posicionamos en canvasDate con Grid
        self.date = tk.Entry(
            master=self.canvasDate,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.date.grid(row=1, column=0, padx=5, pady=5, sticky="WE")

        # Creamos un espacio para que el usuario pueda ingresar una hora, y lo posicionamos en canvasDatecon Grid
        # Lista desplegable que contiene las opciones para View Planets.

        self.astroName = tk.StringVar(self.canvasDate)
        astrosOptions = [
            'Sun',
            'Mercury',
            'Venus',
            'Moon',
            'Mars',
            'Jupiter',
            'Saturn',
            'Uranus',
            'Neptune',
            'Pluto']
        self.astroName.set('Sun')

        self.dicAstros = {
            'Sun': 'sun',
            'Mercury': 'mercury',
            'Venus': 'venus',
            'Moon': 'moon',
            'Mars': 'mars',
            'Jupiter': 'jupiter barycenter',
            'Saturn': 'saturn barycenter',
            'Uranus': 'uranus barycenter',
            'Neptune': 'neptune barycenter',
            'Pluto': 'pluto barycenter'}

        self.astrosList = tk.OptionMenu(
            self.canvasDate, self.astroName, *astrosOptions)
        self.astrosList.grid(row=1, column=1, padx=5, pady=5, sticky="WE")

        # --------------------------------------------
        # Botón que al ser clickeado llamará al método get_times_horizon
        self.img = tk.PhotoImage(
            file=os.path.join(
                ObjectInHorizon.recursos_path,
                'GetRiseAndSetButton.png'))
        self.button = tk.Button(
            self.horizonFrame,
            image=self.img,
            width=340,
            height=42,
            command=self.get_times_horizon)
        self.button.grid(row=3, column=1, padx=5, pady=15)


    def get_times_horizon(self):
        """ Obtiene los tiempos en que el objeto celeste se eleva y se pone por encima del
        horizonte para una ubicación y fecha dadas y los muestra por pantalla
        """

        # Obtener la ubicación, fecha y objeto celeste seleccionado por el
        # usuario
        try: 
            ubicacion, fecha, astro = self.save_data()

            # Utilizar el módulo planetHorizon para obtener los tiempos en que el
            # objeto celeste se eleva y se pone por encima del horizonte
            times = planetHorizon.when_above_horizon(ubicacion, fecha, astro)

            # Crear una etiqueta para cada tiempo y mostrarlo en la interfaz
            # gráfica de usuario
            for i in range(len(times)):
                date_label = tk.Label(
                    self.horizonFrame,
                    text=times[i],
                    font=(
                        "BeVietnamPro-Bold",
                        int(14)),
                    fg="#ffffff",
                    bg="black")
                date_label.grid(
                    row=4 + i,
                    columnspan=3,
                    padx=5,
                    pady=2,
                    sticky='nsew')
                
        except TypeError:
            pass


    def save_data(self):
        ''' Guarda los datos pasados por el usuario

        Obtiene los datos registrados en los objetos tipo Entry y demás, y los guarda
        en los atributos de StarMap
        '''

        # Obtenemos la fecha ingresadas por el usuario
        fecha = self.date.get()

        # Convertimos la fecha y hora a objetos datetime
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')

        except BaseException:
            messagebox.showerror(
                "Error", "Please enter a valid formatted date.")
            return

        # Convertimos el objeto datetime a una cadena de texto y lo guardamos
        # en la variable global
        fecha_str = fecha_obj.strftime('%Y-%m-%d')

        # Obtenemos los valores de los campos de entrada para la ubicación
        pais = self.country.get()
        departamento = self.province.get()
        ciudad = self.city.get()

        if pais == "" or departamento == "" or ciudad == "":
            messagebox.showerror("Error", "Please enter a location.")
            return

        # Unimos los valores en una cadena de texto separada por comas y lo
        # guardamos en la variable global
        ubicacion_str = f"{pais}, {departamento}, {ciudad}"

        # Obtiene el nombre del astro en el formato dado por el diccionario
        astro = self.dicAstros.get(self.astroName.get())

        # Retorna la información solicitada
        return ubicacion_str, fecha_str, astro
