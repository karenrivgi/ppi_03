import tkinter as tk
from Widgets.StarMap import StarMap
import os

class GuestMenu:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def instance_widget(self, widget):
        """Instancia el widget pasado como parametro dentro de la ventana actual"""

        canvasWidgets = tk.Canvas(master = self.mainMenu, width = 764, height = 748)
        canvasWidgets.place(x = 262, y = 20)
        canvasWidgets.update_idletasks()

        widget(master = canvasWidgets)


    def return_to_access(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""
        
        for wid in self.widgets:
            wid.destroy()


    def __init__(self, master: tk.Tk) -> None:
        
        # Creacion del contenedor de los objetos de la ventana.

        self.master = master
        self.widgets = []
        self.mainMenu = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.mainMenu.update_idletasks()
        self.mainMenu.place(x=0, y=0)
        self.widgets.append(self.mainMenu)
        self.background_img = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"GuestBack.png"), master=self.mainMenu) 
        self.background = self.mainMenu.create_image(512, 384, image=self.background_img)
        
        # Creacion de cuadro de texto en el contenedor.

        self.mainMenu.create_text(
            73.5, 41.0,
            text = "Explore",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(25.0)))

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase StarMap.

        self.img2 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"StarMapButton.png"))
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
        # Creacion de boton de para instanciar un widget de clase ObjectSearch.

        self.img1 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"ObjectSearchButton.png"))
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
        # Creacion de boton de para cerrar la sesion y volver al menu de acceso.

        self.img3 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"ReturnButton.png"))
        self.closeSessionButton = tk.Button(
            image = self.img3,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.return_to_access,
            background= "black",
            relief = "flat")

        self.closeSessionButton.place(
            x = 25, y = 609,
            width = 183,
            height = 32)
        self.widgets.append(self.closeSessionButton)
