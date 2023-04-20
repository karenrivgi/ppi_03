import tkinter as tk
from Widgets.StarMap import StarMap
import os
from Widgets.History import History

class MemberMenu:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def instance_widget(self, widget):
        """Instancia el widget pasado como parametro dentro de la ventana actual y destruye el anterior
        en caso de que exista"""
        
        try:
            self.currentWidget.destroy()
        except:
            pass

        self.currentWidget = None

        loadingText = tk.Label(master = self.currentWidgetMaster, text = "Loading...", fg = "white", bg = "black")
        loadingText.place(x = 352, y = 345)

        self.currentWidget = widget(master = self.currentWidgetMaster, user = self.user)
        self.currentWidgetMaster.config(width=764, height=750, background= "black")
        self.currentWidgetMaster.update_idletasks()
        
        loadingText.destroy()


    def close_session(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""

        self.mainMenu.destroy()


    def __init__(self, master: tk.Tk, user = None) -> None:
        
        # Creacion del contenedor de los objetos de la ventana y referencia a la cuenta de usuario.

        self.user = user
        self.mainMenu = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.mainMenu.update_idletasks()
        self.mainMenu.place(x=0, y=0)
        self.background_img = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MemberMenuBack.png"), master=self.mainMenu) 
        self.background = self.mainMenu.create_image(512, 384, image=self.background_img)

        self.currentWidgetMaster = tk.Canvas(master = self.mainMenu)
        self.currentWidgetMaster.place(x = 250, y = 10)
        self.currentWidget = None
        
        
        # Creacion de cuadros de texto en el contenedor.

        self.mainMenu.create_text(
            73.5, 41.0,
            text = "Explore",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(25.0)))

        self.mainMenu.create_text(
            67.0, 420.0,
            text = "Profile",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(25.0)))

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase StarMap.

        self.img2 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"StarMapButton.png"))
        self.starMapButton = tk.Button(
            master = self.mainMenu,
            image = self.img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.starMapButton.place(
            x = 25, y = 80,
            width = 184,
            height = 30)        
        

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase Newsfeed.

        self.img0 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"NewsfeedButton.png"))
        
        self.newsfeedButton = tk.Button(
            master = self.mainMenu,
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")
        
        self.newsfeedButton.place(
            x = 25, y = 180,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase ObjectSearch.

        self.img1 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"ObjectSearchButton.png"))
        self.objectSearchButton = tk.Button(
            master = self.mainMenu,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.objectSearchButton.place(
            x = 25, y = 130,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para cerrar sesion y vovler al menu de acceso.

        self.img3 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"CloseSessionButton.png"))
        self.closeSessionButton = tk.Button(
            master = self.mainMenu,
            image = self.img3,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.close_session(),
            background= "black",
            relief = "flat")

        self.closeSessionButton.place(
            x = 25, y = 659,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para entrar a historiales.

        self.img7 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"HistorialButton.png"))
        self.historialButton = tk.Button(
            master = self.mainMenu,
            image = self.img7,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(History),
            background= "black",
            relief = "flat")

        self.historialButton.place(
            x = 25, y = 559,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase AccountSettings.

        self.img4 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"SettingsButton.png"))
        self.settingsButton = tk.Button(
            master = self.mainMenu,
            image = self.img4,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.settingsButton.place(
            x = 25, y = 609,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MyStars.

        self.img5 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MyStarsButton.png"))
        self.myStarsButton = tk.Button(
            master = self.mainMenu,
            image = self.img5,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.myStarsButton.place(
            x = 25, y = 509,
            width = 184,
            height = 30)
        

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MyMaps.

        self.img6 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MyMapsButton.png"))
        self.myMapsButton = tk.Button(
            master = self.mainMenu,
            image = self.img6,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.myMapsButton.place(
            x = 25, y = 459,
            width = 184,
            height = 30)    
        
