import tkinter as tk
from Widgets.StarMap import StarMap
import os

class MemberMenu:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def instance_widget(self, widget):
        """Instancia el widget pasado como parametro dentro de la ventana actual"""

        for item in self.canvasWidgets.winfo_children():
            item.destroy()

        self.canvasWidgets.config(width=764, height=748)
        widget(master = self.canvasWidgets, user = self.user)


    def close_session(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""

        for wid in self.widgets:
            wid.destroy() 


    def __init__(self, master: tk.Tk, user = None) -> None:
        
        # Creacion del contenedor de los objetos de la ventana y referencia a la cuenta de usuario.

        self.user = user
        self.widgets = []
        self.mainMenu = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.mainMenu.update_idletasks()
        self.mainMenu.place(x=0, y=0)
        self.widgets.append(self.mainMenu)
        self.background_img = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MainMenuBack.png"), master=self.mainMenu) 
        self.background = self.mainMenu.create_image(512, 384, image=self.background_img)
        
        self.canvasWidgets = tk.Canvas(master = self.mainMenu, width = 0, height = 0)
        self.canvasWidgets.place(x = 262, y = 20)
        self.canvasWidgets.update_idletasks()
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
            image = self.img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.instance_widget(StarMap),
            background= "black",
            relief = "flat")

        self.starMapButton.place(
            x = 25, y = 80,
            width = 109,
            height = 32)        
        self.widgets.append(self.starMapButton)

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase Newsfeed.

        self.img0 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"NewsButton.png"))
        
        self.newsfeedButton = tk.Button(
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")
        
        self.newsfeedButton.place(
            x = 25, y = 180,
            width = 119,
            height = 32)
        self.widgets.append(self.newsfeedButton)

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase ObjectSearch.

        self.img1 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"ObjectSearchButton.png"))
        self.objectSearchButton = tk.Button(
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")

        self.objectSearchButton.place(
            x = 25, y = 130,
            width = 171,
            height = 32)
        self.widgets.append(self.objectSearchButton)

        #--------------------------------------------------
        # Creacion de boton de para cerrar sesion y vovler al menu de acceso.

        self.img3 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"CloseButton.png"))
        self.closeSessionButton = tk.Button(
            image = self.img3,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.close_session,
            background= "black",
            relief = "flat")

        self.closeSessionButton.place(
            x = 25, y = 609,
            width = 163,
            height = 32)
        self.widgets.append(self.closeSessionButton)

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase AccountSettings.

        self.img4 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"SettingsButton.png"))
        self.settingsButton = tk.Button(
            image = self.img4,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")

        self.settingsButton.place(
            x = 25, y = 559,
            width = 98,
            height = 32)
        self.widgets.append(self.settingsButton)

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MyStars.

        self.img5 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"StarsButton.png"))
        self.myStarsButton = tk.Button(
            image = self.img5,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")

        self.myStarsButton.place(
            x = 25, y = 509,
            width = 103,
            height = 32)
        self.widgets.append(self.myStarsButton)

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase MyMaps.

        self.img6 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MapsButton.png"))
        self.myMapsButton = tk.Button(
            image = self.img6,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")

        self.myMapsButton.place(
            x = 25, y = 459,
            width = 106,
            height = 32)    
        self.widgets.append(self.myMapsButton)   
