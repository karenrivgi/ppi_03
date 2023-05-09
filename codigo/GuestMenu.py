import tkinter as tk
from Widgets.StarMap import StarMap
import os


class GuestMenu:

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__), "Recursos")
    # Creación variable "canvasWidgets " con valor inicial "None".
    canvasWidgets = None

    def instance_widget(self, widget):
        """
        Instancia el widget pasado como parametro dentro de la ventana actual y destruye el anterior
        en caso de que exista.
        """

        # Try que elimina el widget anterior, en caso del except no realizará ninguna acción.
        try:
            self.currentWidget.destroy()
        except:
            pass

        # Creación variable "currentWidget" con valor inicial "None".
        self.currentWidget = None

        # Variable que contiene un Label con texto.
        loadingText = tk.Label(
            master=self.currentWidgetMaster, text="Loading...", fg="white", bg="black")
        loadingText.place(x=352, y=345)  # Posiciona el label.

        # Se crea el widget con parametro master y user con valor inicial "None".
        self.currentWidget = widget(master=self.currentWidgetMaster, user=None)

        # Se configura el tamaño y fondo del widget.
        self.currentWidgetMaster.config(
            width=764, height=750, background="black")
        
        # Forza la actualización del widget.
        self.currentWidgetMaster.update_idletasks()

        loadingText.destroy()  # Destruye el label "loadingText"

    def close_session(self):
        """
        Instancia una ventana de clase AccessMenu y destruye la ventana actual

        Parámetro:
        - self.
        """

        self.mainMenu.destroy()

    def __init__(self, master: tk.Tk) -> None:
        '''
        Función que crea una ventana gráfica para la clase GuestMenu, donde se encuentran el contenedor
        principal que incluye dentro de este, otro contenedor para el Widget StarMap y dos botones:
        -"closeSessionButton" para llamar a la función close_session
        - "starMapButton" para llamar al Widget StarMap.

        Parámetros:
        - self.
        - master.
        '''

        # Creacion del contenedor de los objetos de la ventana.

        self.master = master  # Creación variable user que almacena la clase "user".
        self.mainMenu = tk.Canvas(master, width=master.winfo_width(), height=master.winfo_height(
        ), bd=0, highlightthickness=0, relief="ridge", bg="black")  # Creación del contenedor principal tipo Canvas.
        self.mainMenu.update_idletasks()  # Forzar actualizar contenedor.
        self.mainMenu.place(x=0, y=0)  # Posicionamiento contenedor.

        # Creación variable "background_img" que almacena la imagen "GuestSessionBack.png".
        self.background_img = tk.PhotoImage(file=os.path.join(
            GuestMenu.recursos_path, "GuestSessionBack.png"), master=self.mainMenu)
        
        # Creación variable que almacena el contenedor agregandole el fondo de la variable "backgroun_img".
        self.background = self.mainMenu.create_image(
            512, 384, image=self.background_img)
        
        # Creación del contenedor hijo "currentWidgetMaster" tipo Canvas que tendrá dentro uno de los widgets instanciados por medio de los botones.
        self.currentWidgetMaster = tk.Canvas(
            master=self.mainMenu, width=0, height=0)
        
        # Posicionamiento widget "currentWidgetMaster".
        self.currentWidgetMaster.place(x=250, y=10)

        # Creación variable "currentWidget" con valor inicial "None".
        self.currentWidget = None

        # -----------------------------------------------
        # Creacion de cuadros de texto en el contenedor.

        self.mainMenu.create_text(
            73.5, 41.0,
            text="Explore",
            fill="#ffffff",
            font=("BeVietnamPro-Bold", int(25.0)))  # Creacion de cuadro de texto "Explore".

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase StarMap.

        # Asigna la imagen "StarMapButtonG.png" a la variable "img2".
        self.img2 = tk.PhotoImage(file=os.path.join(
            GuestMenu.recursos_path, "StarMapButtonG.png"))
        self.starMapButton = tk.Button(
            master=self.mainMenu,
            image=self.img2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(StarMap),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "StarMap".
        self.starMapButton.place(
            x=25, y=80,
            width=150,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para cerrar la sesion y volver al menu de acceso.

        # Asigna la imagen "ReturnToMenuG.png" a la variable "img3".
        self.img3 = tk.PhotoImage(file=os.path.join(
            GuestMenu.recursos_path, "ReturnToMenuG.png"))
        self.closeSessionButton = tk.Button(
            master=self.mainMenu,
            image=self.img3,
            borderwidth=0,
            highlightthickness=0,
            command=self.close_session,
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "close_session()".
        self.closeSessionButton.place(
            x=25, y=659,
            width=196,
            height=42)  # Posicionamiento del Botón en el contenedor principal.