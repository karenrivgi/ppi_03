import tkinter as tk
import os
from Widgets.StarMap import StarMap
from Widgets.History import History
from Widgets.Newsfeed import Newsfeed
from Widgets.ObjectSearch import ObjectSearch
from Widgets.MyAstros import MyAstros
from Widgets.MoonPhase import MoonPhase


class MemberMenu:
    '''
    Clase "MemberMenu" que contiene la variable que referencia al directorio con los recursos gráficos,
    también contiene las funciones:
    - instance_widget()
    - close_session()
    - __init__()
    '''

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__), "Recursos")

    def instance_widget(self, widget):
        """
        Instancia el widget pasado como parametro dentro de la ventana actual y destruye el anterior
        en caso de que exista

        Parámetros:
        - self
        - widget
        """

        # Try que elimina el widget anterior, en caso del except no realizará ninguna acción.
        try:
            # self.currentWidget.destroy()
            for child in self.currentWidgetMaster.winfo_children():
                child.destroy()
        except:
            pass

        # self.currentWidget = None

        # Configura tamaño y fondo del widget "currentWidgetMaster".
        self.currentWidgetMaster.config(
            width=764, height=750, background="black")
        
        # Crea un Label que contiene la palabra "Loading".
        loadingText = tk.Label(
            master=self.currentWidgetMaster, text="Loading...", fg="white", bg="black")
        
        loadingText.place(x=352, y=345)  # Posicona el Label.
        # Forza la actualización del widget.
        self.currentWidgetMaster.update_idletasks()

        # Crea la variable "currentWidget" que almacena un widget con parametros del widget "currentWidgetMaster" y "user".
        self.currentWidget = widget(
            master=self.currentWidgetMaster, user=self.user)

        # loadingText.destroy()

    def close_session(self):
        """
        Instancia una ventana de clase AccessMenu y destruye la ventana actual

        Parámetro:
        - self.
        """
        self.mainMenu.destroy()

    def __init__(self, master: tk.Tk, user=None) -> None:
        '''
        Esta función crea una ventana gráfica para la clase MemberMenu, donde se encuentran el contenedor
        principal que incluye dentro de este: dos cuadros de texto "Explore y "Profile",
        seis botones: starMapButton, newsfeedButton, objectSearchButton, moonphaseButton,
        historialButton, myStarsButton y  closeSessionButton, 
        también contiene otro contenedor que instancia un Widget al ser apretado por uno de los siguientes botones:
        - "starMapButton" que llama la función instance_widget tomando como arguemento la clase "StarMap"
        - "newsfeedButton" que llama la función instance_widget tomando como arguemento la clase "Newsfeed"
        - "objectSearchButton" que llama la función instance_widget tomando como arguemento la clase "ObjectSearch"
        - "moonPhaseButton" que llama la función instance_widget tomando como arguemento la clase "MoonPhase"
        - "historialButton" que llama la función instance_widget tomando como arguemento la clase "History"
        - "myStarsButton" que llama la función instance_widget tomando como arguemento la clase "MyAstros",
        exceptuando por el botón que llama la función close_session.
        '''

        # Creacion del contenedor de los objetos de la ventana y referencia a la cuenta de usuario.

        self.user = user  # Creación variable user que almacena la clase "user".
        self.mainMenu = tk.Canvas(master, width=master.winfo_width(), height=master.winfo_height(
        ), bd=0, highlightthickness=0, relief="ridge", bg="black")  # Creación del contenedor principal tipo Canvas.

        self.mainMenu.update_idletasks()  # Forzar actualizar contenedor.

        self.mainMenu.place(x=0, y=0)  # Posicionamiento contenedor.

        # Creación variable "background_img" que almacena la imagen "MemberMenuBack.png"
        self.background_img = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "MemberMenuBack.png"), master=self.mainMenu)
        
        # Creación variable que almacena el contenedor agregandole el fondo de la variable "backgroun_img"
        self.background = self.mainMenu.create_image(
            512, 384, image=self.background_img)
        
        # Creación del contenedor hijo "currentWidgetMaster" tipo Canvas que tendrá dentro uno de los widgets instanciados por medio de los botones.
        self.currentWidgetMaster = tk.Canvas(
            master=self.mainMenu, width=0, height=0, highlightthickness=0)
        
        # Posicionamiento widget "currentWidgetMaster".
        self.currentWidgetMaster.place(x=250, y=10)

        # Creación varaible "currentWidget" con valor inicial "None".
        self.currentWidget = None

        # -----------------------------------------------
        # Creacion de cuadros de texto en el contenedor.

        self.mainMenu.create_text(
            73.5, 41.0,
            text="Explore",
            fill="#ffffff",
            font=("BeVietnamPro-Bold", int(25.0)))  # Cuadro de Texto "Explore".

        self.mainMenu.create_text(
            67.0, 420.0,
            text="Profile",
            fill="#ffffff",
            font=("BeVietnamPro-Bold", int(25.0)))  # Cuadro de Texto "Profile".

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase Newsfeed.

        # Asigna la imagen "NewsfeedButton.png" a la variable "img0".
        self.img0 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "NewsfeedButton.png"))
        self.newsfeedButton = tk.Button(
            master=self.mainMenu,
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(Newsfeed),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "Newsfeed".
        self.newsfeedButton.place(
            x=25, y=180,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase ObjectSearch.

        # Asigna la imagen "ObjectSearchButton.png" a la variable "img1".
        self.img1 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "ObjectSearchButton.png"))
        self.objectSearchButton = tk.Button(
            master=self.mainMenu,
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(ObjectSearch),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "ObjectSearch".
        self.objectSearchButton.place(
            x=25, y=130,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase StarMap.

        # Asigna la imagen "StarMapButton.png" a la variable "img2".
        self.img2 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "StarMapButton.png"))
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
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para cerrar sesion y vovler al menu de acceso.

        # Asigna la imagen "CloseSessionButton.png" a la variable "img3".
        self.img3 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "CloseSessionButton.png"))
        self.closeSessionButton = tk.Button(
            master=self.mainMenu,
            image=self.img3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.close_session(),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "close_session()".
        self.closeSessionButton.place(
            x=25, y=609,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase AccountSettings.
        '''
        # Asigna la imagen "SettingsButton.png" a la variable "img4".
        self.img4 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "SettingsButton.png"))
        self.settingsButton = tk.Button(
            master=self.mainMenu,
            image=self.img4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(StarMap),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "StarMap".
        self.settingsButton.place(
            x=25, y=559,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.
        '''

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MyAstros.

        # Asigna la imagen "MyAstrosButton.png" a la variable "img5".
        self.img5 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "MyAstrosButton.png"))
        self.myStarsButton = tk.Button(
            master=self.mainMenu,
            image=self.img5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(MyAstros),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "MyAstros".
        self.myStarsButton.place(
            x=25, y=459,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para entrar a historiales.

        # Asigna la imagen "HistorialButton.png" a la variable "img7".
        self.img7 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "HistorialButton.png"))
        self.historialButton = tk.Button(
            master=self.mainMenu,
            image=self.img7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(History),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "History".
        self.historialButton.place(
            x=25, y=509,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MoonPhase

        # Asigna la imagen "MoonPhaseButton.png" a la variable "img8".
        self.img8 = tk.PhotoImage(file=os.path.join(
            MemberMenu.recursos_path, "MoonPhaseButton.png"))
        self.moonPhaseButton = tk.Button(
            image=self.img8,
            master=self.mainMenu,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.instance_widget(MoonPhase),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "instance_widget()" que tiene como argumento la clase "MoonPhase".
        self.moonPhaseButton.place(
            x=25, y=230,
            width=184,
            height=30)  # Posicionamiento del Botón en el contenedor principal.