import calendar
import os
import webbrowser
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from os.path import abspath, dirname, join
from StarMapGenerator import MoonPhaseSearch


class MoonPhase:

    recursos_path = join(dirname(dirname(abspath(__file__))), "Recursos")

    def __init__(self, master: tk.Tk, user=None):
        """ Constructor de la clase MoonPhase.

        Args:
        - master: objeto Tk raíz para la aplicación.
        - user: parámetro opcional que no se utiliza en esta implementación.
        """
        # Canvas base
        self.moonCanvas = tk.Canvas(
            master,
            width=764,
            height=732,
            background="black",
            highlightthickness=0)
        self.moonCanvas.place(x=0, y=0, relwidth=1, relheight=1, anchor='nw')

        # Se crean los widgets (labels, campos de entrada y botón).
        self.create_widgets()

    def destroy(self):
        """ Destruye el canvas principal de la aplicación. """
        self.moonCanvas.destroy()

    def create_widgets(self):
        """ Crea los widgets de la interfaz de usuario de la aplicación. """

        # Frame principal donde se colocarán los widgets.
        self.moonFrame = tk.Frame(
            self.moonCanvas,
            width=764,
            height=732,
            background="black",
            highlightthickness=0)
        self.moonFrame.update_idletasks()
        self.moonFrame.grid(
            row=0,
            column=0,
            padx=45,
            pady=10,
            sticky="NSEW",
        )

        # Label para el encabezado de la interfaz.
        self.header_label = tk.Label(
            self.moonFrame,
            text="What phase is the Moon?",
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

        # Label y campo de entrada para el año.
        self.year_label = tk.Label(
            self.moonFrame,
            text="Year (YYYY)",
            font=("BeVietnamPro 12"),
            fg="#ffffff",
            bg="black",
            highlightthickness=0,
            width=23)
        self.year_label.grid(row=1, column=0, padx=5, pady=5, sticky="WE")

        self.year_entry = tk.Entry(
            self.moonFrame,
            font=("BeVietnamPro 12"),
            fg="black",
            bg="white",
            highlightthickness=0,
            bd=0,
            width=23)
        self.year_entry.grid(row=2, column=0, padx=5, pady=5, sticky="WE")

        # Label y campo de entrada para el mes.
        self.month_label = tk.Label(
            self.moonFrame,
            text="Month (M)",
            font=("BeVietnamPro 12"),
            fg="#ffffff",
            bg="black",
            highlightthickness=0,
            width=23)
        self.month_label.grid(row=1, column=1, padx=5, pady=5, sticky="WE")

        self.month_entry = tk.Entry(
            self.moonFrame,
            font=("BeVietnamPro 12"),
            fg="black",
            bg="white",
            highlightthickness=0,
            bd=0,
            width=23)
        self.month_entry.grid(row=2, column=1, padx=5, pady=5, sticky="WE")

        # Label y campo de entrada para el día.
        self.day_label = tk.Label(
            self.moonFrame,
            text="Day (D)",
            font=("BeVietnamPro 12"),
            fg="white",
            bg="black",
            highlightthickness=0,
            width=23)

        self.day_label.grid(row=1, column=2, padx=5, pady=5, sticky="WE")

        self.day_entry = tk.Entry(
            self.moonFrame,
            font=("BeVietnamPro 12"),
            fg="black",
            bg="white",
            highlightthickness=0,
            bd=0,
            width=23)
        self.day_entry.grid(row=2, column=2, padx=5, pady=5, sticky="WE")

        # Botón que al ser clickeado llamará al método get_moon_phase
        self.img = tk.PhotoImage(
            file=os.path.join(
                MoonPhase.recursos_path,
                'GetMoonPhaseButton.png'))
        self.button = tk.Button(
            self.moonFrame,
            image=self.img,
            width=215,
            height=35,
            command=self.get_moon_phase,
            highlightthickness=0,
            bd=0)
        self.button.grid(row=3, column=1, padx=5, pady=15, sticky='nsew')

    def get_moon_phase(self):
        """ Método que obtiene la fase lunar y la muestra en la interfaz
        gráfica de usuario.

        Returns:
            None
        """

        # VALIDACIONES DE INPUTS ---------------------------------------
        # Setear valores por defecto
        is_invalid = False
        year = 2023
        month = 5
        day = 2

        # Obtener el año de la entrada del usuario y validarla
        try:
            year = int(self.year_entry.get())
            if year < 1900 or year > 2052:
                is_invalid = True
                raise ValueError("The year should be between 1900 and 2052")
        except ValueError as e:
            is_invalid = True
            messagebox.showerror("Error", str(e))

        # Obtener el mes de la entrada del usuario y validarla
        try:
            month = int(self.month_entry.get())
            if month < 1 or month > 12:
                is_invalid = True
        except ValueError as e:
            is_invalid = True
            messagebox.showerror("Error", str(e))

        # Obtener el dia de la entrada del usuario y validarla
        try:
            day = int(self.day_entry.get())
            days_in_month = calendar.monthrange(year, month)[1]
            if day < 1 or day > days_in_month:
                is_invalid = True
                raise ValueError(
                    f"The day should be between 1 and {days_in_month}.")
        except ValueError as e:
            is_invalid = True
            messagebox.showerror("Error", str(e))

        # Terminar el método si algun input es inválido
        if is_invalid:
            return

        # OBTENCIÓN DE RESULTADOS Y MUESTRA EN LA INTERFAZ --------------------
        # Obtener la fase, el porcentaje ilumnado y el numero de la imagen correspondiente
        # con el archivo MoonPhaseSearch
        phase, percent_illuminated, image = MoonPhaseSearch.moon_phase(
            year, month, day, 18, 0)

        # Configurar la fila 1 para que tenga un tamaño de 20 píxeles y usarla
        # como separador
        self.moonFrame.grid_rowconfigure(4, minsize=60)

        # Agregar un tìtulo al moonFrame
        title_text = f"MOON PHASE FOR"
        self.title_label = tk.Label(self.moonFrame, text=title_text, font=(
            "BeVietnamPro-Bold", int(20), 'bold'), fg="#ffffff", bg="black")
        self.title_label.grid(
            row=6,
            columnspan=self.moonFrame.grid_size()[1],
            padx=5,
            pady=2,
            sticky='nsew')

        # Agregar la fecha en la que se buscó la fase lunar
        date_text = f"{year} {calendar.month_name[month]} {day:02d}"
        self.date_label = tk.Label(
            self.moonFrame,
            text=date_text,
            font=(
                "BeVietnamPro-Bold",
                int(14)),
            fg="#ffffff",
            bg="black")
        self.date_label.grid(
            row=7,
            columnspan=self.moonFrame.grid_size()[1],
            padx=5,
            pady=2,
            sticky='nsew')

        # Cargar la imagen de la fase lunar
        phases_path = join(
            join(
                dirname(
                    dirname(
                        abspath(__file__))),
                'StarMapGenerator'),
            'Moons')
        image_path = join(phases_path, f"{image}.png")
        moon_phase_image = Image.open(image_path)
        moon_phase_image = moon_phase_image.resize((250, 250))
        moon_phase_photo = ImageTk.PhotoImage(moon_phase_image)

        # Agregar la imagen al frame contenedor
        self.moon_phase_label = tk.Label(
            self.moonFrame, image=moon_phase_photo, bg="black")
        self.moon_phase_label.image = moon_phase_photo
        self.moon_phase_label.grid(
            row=8,
            columnspan=self.moonFrame.grid_size()[1],
            padx=5,
            pady=10)

        # Diccionario para saber la fase lunar en base a la imagen
        moon_phases = {
            0: "New Moon",
            4: "Last Quarter",
            7: "Waning Gibbous",
            8: "Full Moon",
            10: "Waxing Gibbous",
            12: "First Quarter",
            15: "Waxing Crescent",
            1: "Waning Crescent"
        }

        # Obtener la fase correspondiente si la hay
        phase_name = moon_phases.get(image, "")

        # Agregar label para la fase de la luna
        subtitle_text = phase_name
        self.subtitle_label = tk.Label(
            self.moonFrame,
            text=subtitle_text,
            font=(
                "BeVietnamPro-Bold",
                int(14),
                'bold'),
            fg="#ffffff",
            bg="black")
        self.subtitle_label.grid(
            row=9,
            columnspan=self.moonFrame.grid_size()[1],
            padx=5,
            pady=5,
            sticky='nsew')

        # Agregar label para la fase lunar en grados y el porcentaje de
        # ilumnación
        degrees_text = f"Phase: {phase:.2f}°     Percent Illuminated: {percent_illuminated:.2f}%"
        self.degrees_label = tk.Label(
            self.moonFrame,
            text=degrees_text,
            font=(
                "BeVietnamPro-Bold",
                int(14)),
            fg="#ffffff",
            bg="black")
        self.degrees_label.grid(
            row=10,
            columnspan=self.moonFrame.grid_size()[1],
            padx=5,
            pady=5,
            sticky="nsew")
