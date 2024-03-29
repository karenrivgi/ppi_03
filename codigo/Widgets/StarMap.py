import datetime
import tkinter as tk
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from StarMapGenerator import skymap
from tkinter import filedialog
from os.path import abspath, dirname, join
from api_reddit.make_posts_reddit import make_post
from Widgets.MapInfo import MapInfo


class StarMap:

    # Define la ruta absoluta del directorio donde se encuentra la carpeta
    # Recursos
    recursos_path = join(dirname(dirname(abspath(__file__))), "Recursos")

    def destroy(self):
        self.starMap.destroy()

    def instance_widget(self):
        """Instancia el widget pasado como parametro dentro de la ventana actual y destruye el anterior
        en caso de que exista"""

        try:
            self.canvasDate.destroy()
            self.buttonParent.destroy()
            self.figMaster.destroy()
            self.canvasPosition.destroy()
            self.canvasPosition2.destroy()
            self.starMap.grid_forget()
            self.starMap.update_idletasks()
        except BaseException:
            pass

        MapInfo(master=self.starMap, estrellas=self.nombres_estrellas,
                planeta=self.planet, constelacion=self.culture, user=self.user)

    def __init__(self, master: tk.Canvas, user=None) -> None:

        # Para llevar control de si tenemos un usuario registrado o no
        self.user = user

        # -------------------------------------
        # Canvas contenedor
        self.starMap = tk.Canvas(
            master,
            width=764,
            height=750,
            background="black",
            highlightthickness=0)
        self.starMap.update_idletasks()
        # self.starMap.grid(sticky="nsew")
        master.create_window((0, 0), window=self.starMap, anchor="nw")

        # -------------------------------------
        # Canvas donde posicionaremos los botones y labels para obtener
        # información sobre la ubicación
        self.canvasPosition = tk.Frame(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.canvasPosition.update_idletasks()
        self.canvasPosition.grid(row=0, column=0, sticky="nsew")
        self.canvasPosition.grid_anchor("center")

        # Posicionamos el Label para el país en canvasPosition, usando grid
        self.countryText = tk.Label(
            self.canvasPosition,
            text="Country",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff",
            bg="black")

        self.countryText.grid(row=0, column=0)

        # Posicionamos el Label para la providencia en canvasPosition, usando
        # grid
        self.provinceText = tk.Label(
            self.canvasPosition,
            text="Province",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff", bg="black")
        self.provinceText.grid(row=0, column=1)

        # Posicionamos el Label para la ciudad en canvasPosition, usando grid
        self.cityText = tk.Label(
            self.canvasPosition,
            text="City",
            font=("BeVietnamPro-Bold", int(12)),
            width=15,
            fg="#ffffff",
            bg="black"
        )
        self.cityText.grid(row=0, column=2)

        # Creamos un espacio para que el usuario pueda ingresar su país, y lo
        # posicionamos en canvasPosition con Grid
        self.country = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.country.grid(row=1, column=0, padx=5, pady=5)

        # Creamos un espacio para que el usuario pueda ingresar su providencia,
        # y lo posicionamos en canvasPosition con Grid
        self.province = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.province.grid(row=1, column=1, padx=5, pady=5)

        # Creamos un espacio para que el usuario pueda ingresar su ciudad, y lo
        # posicionamos en canvasPosition con Grid
        self.city = tk.Entry(
            master=self.canvasPosition,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15
        )
        self.city.grid(row=1, column=2, padx=5, pady=5)

        # -------------------------------------
        # Canvas donde posicionaremos los botones y labels para obtener
        # información sobre la fecha y hora
        self.canvasDate = tk.Frame(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.canvasDate.update_idletasks()
        self.canvasDate.grid(row=1, column=0, sticky="nsew")
        self.canvasDate.grid_anchor("center")

        # Posicionamos el Label para la fecha en canvasDate, usando grid
        self.dateText = tk.Label(
            self.canvasDate,
            text="Date (AAAA-MM-DD)",
            font=("BeVietnamPro-Bold", int(12)),
            width=18,
            fg="#ffffff",
            bg="black")
        self.dateText.grid(row=0, column=0)

        # Posicionamos el Label para la hora en canvasDate, usando grid
        self.hourText = tk.Label(
            self.canvasDate,
            text="Hour (HH:MM)",
            font=("BeVietnamPro-Bold", int(12)),
            width=18,
            fg="#ffffff",
            bg="black")
        self.hourText.grid(row=0, column=1)

        # Creamos un espacio para que el usuario pueda ingresar una fecha, y lo
        # posicionamos en canvasDate con Grid
        self.date = tk.Entry(
            master=self.canvasDate,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15)
        self.date.grid(row=1, column=0, padx=5, pady=5)

        # Creamos un espacio para que el usuario pueda ingresar una hora, y lo
        # posicionamos en canvasDatecon Grid
        self.hour = tk.Entry(
            master=self.canvasDate,
            bd=0,
            highlightthickness=0,
            font=("BeVietnamPro 12"),
            width=15)
        self.hour.grid(row=1, column=1, padx=5, pady=5)

        # -------------------------------------
        # buttonParent es un canvas donde posicionaremos los distintos botones
        self.buttonParent = tk.Frame(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.buttonParent.update_idletasks()
        self.buttonParent.grid(row=2, column=0, sticky="nsew")
        self.buttonParent.grid_anchor("center")

        # Creamos y posicionamos con grid en buttonParent el botón para guardar
        # los datos suministrados
        self.img1 = tk.PhotoImage(
            file=join(
                StarMap.recursos_path,
                "SaveButon.png"))
        self.saveButton = tk.Button(
            master=self.buttonParent,
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_data,
            # Cuando sea presionado, se ejecutará el método save_data de
            # StarMap
            relief="flat",
            bg="black")
        self.saveButton.grid(row=0, column=0, padx=5, pady=5)

        # Creamos y posicionamos con grid en buttonParent el botón para mostrar
        # el gráfico
        self.img0 = tk.PhotoImage(
            file=join(
                StarMap.recursos_path,
                "SubmitButton.png"))
        self.submitButton = tk.Button(
            master=self.buttonParent,
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=self.show_image,
            # Cuando sea presionado, se ejecutará el método show_image de
            # StarMap
            relief="flat",
            state="disabled",
            bg="black")
        self.submitButton.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        # -----------------------
        # BOTONES EXCLUSIVOS PARA USUARIOS REGISTRADOS

        if self.user:

            # Creamos y posicionamos con grid en buttonParent el botón para
            # descargar el gráfico
            self.img2 = tk.PhotoImage(
                file=join(
                    StarMap.recursos_path,
                    "DownloadButton.png"))
            self.downloadButton = tk.Button(
                master=self.buttonParent,
                image=self.img2,
                borderwidth=0,
                highlightthickness=0,
                command=self.save_image,
                # Cuando sea presionado, se ejecutará el método save_image de
                # StarMap
                relief="flat",
                state="disabled",
                bg="black")
            self.downloadButton.grid(row=1, column=0, padx=5, pady=5)

            # Creamos y posicionamos con grid en buttonParent el botón para
            # compartir el gráfico
            self.img3 = tk.PhotoImage(
                file=join(
                    StarMap.recursos_path,
                    "ShareButton.png"))
            self.shareButton = tk.Button(
                master=self.buttonParent,
                image=self.img3,
                borderwidth=0,
                highlightthickness=0,
                command=self.share_image,
                # Cuando sea presionado, se ejecutará el método share_image de
                # StarMap
                relief="flat",
                state="disabled",
                bg="black")
            self.shareButton.grid(row=1, column=1, padx=5, pady=5)

        # ---------------------------
        self.figMaster = tk.Canvas(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.figMaster.update_idletasks()
        self.figMaster.grid(row=3, column=0, sticky="nsew")
        self.figMaster.grid_anchor("s")
        self.figMaster.update_idletasks()

        # -------------------------------------
        # Canvas donde posicionaremos las listas desplegables y textos para la
        # personalizacion del mapa
        self.canvasPosition2 = tk.Frame(
            self.starMap,
            highlightthickness=0,
            background="black")
        self.canvasPosition2.update_idletasks()
        self.canvasPosition2.grid(row=0, column=1, sticky="nsew", rowspan=4)
        self.canvasPosition2.grid_anchor("n")

        self.customizeText = tk.Label(
            self.canvasPosition2,
            text="Customize Map",
            font=("BeVietnamPro-Bold", int(23.0)),
            width=12,
            fg="#ffffff",
            bg="black"
        )
        self.customizeText.grid(row=0, column=0, padx=0, pady=0)

        # Label que contiene una de las funcionalidades de personalización con
        # el texto View Planets
        self.imgViewPlanets = tk.PhotoImage(
            file=os.path.join(
                StarMap.recursos_path,
                "ViewPlanetsButtonF.png"))
        self.viewPlanets = tk.Label(
            self.canvasPosition2,
            width=200,
            image=self.imgViewPlanets,
            bg="black")

        self.viewPlanets.grid(row=1, column=0, padx=0, pady=0)

        # Lista desplegable que contiene las opciones para View Planets.
        self.varViewPlanets = tk.StringVar(self.canvasPosition2)
        opcionesViewPlanets = [
            'Mercury',
            'Venus',
            'Mars',
            'Jupiter',
            'Saturn',
            'Uranus',
            'Neptune',
            'Pluto']
        self.varViewPlanets.set('Mars')
        self.dicViewPlanets = {
            'Mercury': 'mercury',
            'Venus': 'venus',
            'Mars': 'mars',
            'Jupiter': 'jupiter',
            'Saturn': 'saturn',
            'Uranus': 'uranus',
            'Neptune': 'neptune',
            'Pluto': 'pluto'}
        self.listaViewPlanets = tk.OptionMenu(
            self.canvasPosition2,
            self.varViewPlanets,
            *opcionesViewPlanets)
        self.listaViewPlanets.config(width=15)
        self.listaViewPlanets.grid(row=2, column=0)

        # -----------------------
        # OPCIONES DE PERSONALIZACIÓN EXCLUSIVAS PARA USUARIOS REGISTRADOS
        if self.user:

            # Label que contiene una de las funcionalidades de personalización
            # con el texto Astros Name
            self.imgShowAstrosNames = tk.PhotoImage(
                file=os.path.join(
                    StarMap.recursos_path,
                    "AstrosNameButtonF.png"))
            self.showAstrosNames = tk.Label(
                self.canvasPosition2,
                width=200,
                image=self.imgShowAstrosNames,
                bg="black")
            self.showAstrosNames.grid(row=3, column=0, pady=5)

            # Lista desplegable que contiene las opciones para Astros Name.
            self.varAstrosNames = tk.StringVar(self.canvasPosition2)
            opcionesAstrosNames = ['Yes', 'No']
            self.varAstrosNames.set('No')
            self.dicAstrosNames = {'Yes': True, 'No': False}
            self.listaAstrosNames = tk.OptionMenu(
                self.canvasPosition2, self.varAstrosNames, *opcionesAstrosNames)
            self.listaAstrosNames.config(width=15)
            self.listaAstrosNames.grid(row=4, column=0)

            # Label que contiene una de las funcionalidades de personalización
            # con el texto Stars Amount.
            self.imgStarsAmount = tk.PhotoImage(
                file=os.path.join(
                    StarMap.recursos_path,
                    "StarsAmountButtonF.png"))
            self.starsAmount = tk.Label(
                self.canvasPosition2,
                width=180,
                image=self.imgStarsAmount,
                bg="black")
            self.starsAmount.grid(row=5, column=0, pady=5)

            # Lista desplegable que contiene las opciones para Stars Amount.
            self.varStarsAmount = tk.StringVar(self.canvasPosition2)
            opcionesStarsAmount = ['Default', 'Many stars']
            self.varStarsAmount.set('Default')
            self.dicStarsAmount = {'Default': 5, 'Many stars': 25}
            self.listaStarsAmount = tk.OptionMenu(
                self.canvasPosition2, self.varStarsAmount, *opcionesStarsAmount)
            self.listaStarsAmount.config(width=15)
            self.listaStarsAmount.grid(row=6, column=0)

            # Label que contiene una de las funcionalidades de personalización
            # con el texto Constellations Culture.
            self.imgConstellationsCulture = tk.PhotoImage(file=os.path.join(
                StarMap.recursos_path, "ConstellationsCultureButtonF.png"))
            self.constellationsCulture = tk.Label(
                self.canvasPosition2,
                width=200,
                image=self.imgConstellationsCulture,
                bg="black")
            self.constellationsCulture.grid(row=7, column=0, pady=5)

            # Lista desplegable que contiene las opciones para Constellations
            # Culture.
            self.varConstellationsCulture = tk.StringVar(self.canvasPosition2)
            opcionesConstellationsCulture = [
                'Moderna', 'Maya', 'Chinese', 'Egyptian']
            self.varConstellationsCulture.set('Moderna')
            self.dicConsCulture = {
                'Moderna': 'modern',
                'Maya': 'maya',
                'Chinese': 'chinese',
                'Egyptian': 'egyptian'}
            self.listaConstellationsCulture = tk.OptionMenu(
                self.canvasPosition2,
                self.varConstellationsCulture,
                *opcionesConstellationsCulture)
            self.listaConstellationsCulture.config(width=15)
            self.listaConstellationsCulture.grid(row=8, column=0)

            # Label que contiene una de las funcionalidades de personalización
            # con el texto Constellations Color.
            self.imgConstellationsColor = tk.PhotoImage(file=os.path.join(
                StarMap.recursos_path, "ConstellationsColorButtonF.png"))
            self.constellationsColor = tk.Label(
                self.canvasPosition2,
                width=200,
                image=self.imgConstellationsColor,
                bg="black")
            self.constellationsColor.grid(row=9, column=0, pady=5)

            # Lista desplegable que contiene las opciones para Constellations
            # Color.
            self.varConstellationsColor = tk.StringVar(self.canvasPosition2)
            opcionesConstellationsColor = [
                'Yellow', 'Green', 'Blue', 'Red', 'White', 'Cyan', 'Magenta']
            self.varConstellationsColor.set('Yellow')
            self.dicConsColor = {
                'Yellow': 'y',
                'Green': 'g',
                'Blue': 'b',
                'Red': 'r',
                'White': 'w',
                'Cyan': 'c',
                'Magenta': 'm'}
            self.listaConstellationsColor = tk.OptionMenu(
                self.canvasPosition2,
                self.varConstellationsColor,
                *opcionesConstellationsColor)
            self.listaConstellationsColor.config(width=15)
            self.listaConstellationsColor.grid(row=10, column=0)

        # Parámetros necesarios para la generación del mapa estelar, con
        # valores por defecto
        self.canvas_skymap = None
        self.skymap = None
        self.fecha_hora_str = None
        self.ubicacion_str = None
        self.magnitud_lim = 8
        self.mostrar_nombres_estrellas = True
        self.planeta = None
        self.cons_color = 'y'
        self.culture = 'modern'
        self.nombres_estrellas = None

        # Creamos y posicionamos con grid en Canvas de CustomizeMap el botón
        # para acceder al widget con la informacion del mapa.
        self.img4 = tk.PhotoImage(
            file=join(
                StarMap.recursos_path,
                "MapInfosButton.png"))
        self.cInfoButton = tk.Button(
            master=self.canvasPosition2,
            image=self.img4,
            command=lambda: self.instance_widget(),
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            state='disabled',
            bg="black")
        self.cInfoButton.grid(row=11, column=0, pady=15)

        info = [
            'You should generate a map with your preferred customization options.',
            'After saving the data, the other buttons will be activated.']
        messagebox.showinfo("To consider.", "\n".join(info))

    # MÉTODOS DE STARMAP

    def save_data(self):
        ''' Guarda los datos pasados por el usuario

        Obtiene los datos registrados en los objetos tipo Entry y demás, y los guarda
        en los atributos de StarMap
        '''

        # Obtenemos la fecha y hora ingresadas por el usuario
        fecha = self.date.get()
        hora = self.hour.get()

        # Convertimos la fecha y hora a objetos datetime
        try:
            fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')

        except BaseException:
            messagebox.showerror(
                "Error", "Please enter a valid formatted date.")
            return

        try:
            hora_obj = datetime.datetime.strptime(hora, '%H:%M')

        except BaseException:
            messagebox.showerror(
                "Error", "Please enter a valid formatted hour.")
            return

        # Combinamos la fecha y hora en un solo objeto datetime
        fecha_hora_obj = fecha_obj.replace(
            hour=hora_obj.hour, minute=hora_obj.minute)

        # Convertimos el objeto datetime a una cadena de texto y lo guardamos
        # en la variable global
        self.fecha_hora_str = fecha_hora_obj.strftime('%Y-%m-%d %H:%M')

        # Obtenemos los valores de los campos de entrada para la ubicación
        pais = self.country.get()
        departamento = self.province.get()
        ciudad = self.city.get()

        if pais == "" or departamento == "" or ciudad == "":
            messagebox.showerror("Error", "Please enter a location.")
            return

        # Unimos los valores en una cadena de texto separada por comas y lo
        # guardamos en la variable global
        self.ubicacion_str = f"{pais}, {departamento}, {ciudad}"

        # Mostramos un mensaje al usuario indicando que los datos han sido
        # guardados
        messagebox.showinfo("Saved", "The data has been saved correctly.")

        # Habilitar el botón "Mostrar gráfico"
        self.submitButton.config(state='normal')

        self.planeta_seleccionado = self.varViewPlanets.get()
        self.planet = self.dicViewPlanets.get(self.planeta_seleccionado)

        # Parametros personalizacion:
        if self.user:
            self.name_seleccionado = self.varAstrosNames.get()
            self.amount_seleccionado = self.varStarsAmount.get()
            self.culture_seleccionada = self.varConstellationsCulture.get()
            self.color_seleccionado = self.varConstellationsColor.get()
            self.magnitud_lim = self.dicStarsAmount.get(
                self.amount_seleccionado)
            self.mostrar_nombres_estrellas = self.dicAstrosNames.get(
                self.name_seleccionado)
            self.cons_color = self.dicConsColor.get(self.color_seleccionado)
            self.culture = self.dicConsCulture.get(self.culture_seleccionada)

    def show_image(self):
        ''' Muestra el gráfico en pantalla en base a los datos suministrados

        Accede a los atributos de StarMap donde se guarda la información necesaria para
        graficar. Llama al método generar_mapa de skymap.py con los parámetros para obtener
        el gráfico, finalmente lo muestra en pantalla al convertirlo en un Canvas.

        Se guarda el historial y se muestran otros botones si se trata de un usuario registrado
        '''

        # Guarda en fig el gráfico generado por skymap.generar_mapa
        try:
            fig, warning, geopy_problem, nombres_estrellas = skymap.generar_mapa(self.fecha_hora_str, self.ubicacion_str,
                                                                                 self.figMaster.winfo_height(), self.magnitud_lim,
                                                                                 self.mostrar_nombres_estrellas, self.planet,
                                                                                 self.cons_color, self.culture)

        except BaseException:
            messagebox.showerror(
                "Location Error",
                "The requested location is invalid, please enter a valid one.")
            self.submitButton.config(state="disabled")
            return

        if warning:
            messagebox.showwarning(
                "Warning", "Perhaps the planet cannot be visualized.")

        if geopy_problem:
            self.ubicacion_str = 'Colombia, Antioquia, Medellin'

        if nombres_estrellas:
            self.nombres_estrellas = nombres_estrellas

        # Si es un usuario registrado, guarda en su historial los datos
        # suministrados para la graficación
        if self.user:
            # Si ese input ya ha sido usado con anterioridad o en repetidas
            # ocasiones, no lo guardamos
            # En este caso, guardamos la fecha de generacion, los datos de generacion, y el estado
            # de no publicado en el subreddit
            if [datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                self.fecha_hora_str,
                self.ubicacion_str,
                    "Not published"] not in self.user.historial:
                self.user.guardar_historial([datetime.datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"), self.fecha_hora_str, self.ubicacion_str, "Not published"])

        # Crea un canvas a partir de fig para poder mostrar el gráfico con
        # tkinter
        if self.canvas_skymap:
            self.canvas_skymap.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.figMaster)
        self.skymap = canvas
        self.canvas_skymap = canvas.get_tk_widget()
        canvas.draw()
        self.canvas_skymap.config(width=524, height=524)
        self.canvas_skymap.grid(column=0, row=0, pady=20)

        # Si se trata de un usuario registrado, activamos los botones para
        # descargar y compartir.
        if self.user:
            self.downloadButton.config(state='normal')
            self.shareButton.config(state='normal')

        # Activa boton MapInfo.
        self.cInfoButton.config(state='normal')

        # Mostrar la ventana de Tkinter
        # self.starMap.mainloop()

    def save_image(self):
        ''' Guarda el gráfico mostrado en los archivos del usuario
        '''

        # Obtener el nombre del archivo y la ubicación donde se guardará la
        # imagen
        filename = filedialog.asksaveasfilename(defaultextension=".png")

        if filename == '':
            return

        # Guardar el archivo en la ruta pasada con el nombre seleccionado
        self.skymap.print_png(filename)

    def share_image(self):

        # Especifica el nombre de archivo completo y la ruta de la imagen a
        # eliminar
        filename = "./map.png"

        self.skymap.print_png(filename)

        title, link = make_post(
            self.user, self.ubicacion_str, self.fecha_hora_str)

        messagebox.showinfo(
            "Shared!",
            "You will be able to see your post on https://www.reddit.com/r/PyMansSky/ in a few minutes.")

        # Actualiza en su historial los datos de la publicación
        self.user.guardar_historial(
            [self.fecha_hora_str, self.ubicacion_str, [title, link]], 'reddit')

        # Verifica si el archivo existe
        if os.path.exists(filename):
            # Elimina el archivo
            os.remove(filename)
