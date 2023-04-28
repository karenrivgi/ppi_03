import tkinter as tk
from Widgets.StarMap import StarMap
import os

class GuestMenu:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")
    canvasWidgets = None

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

        self.currentWidget = widget(master = self.currentWidgetMaster, user = None)
        self.currentWidgetMaster.config(width=764, height=750, background= "black")
        self.currentWidgetMaster.update_idletasks()
        
        loadingText.destroy()


    def close_session(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""

        self.mainMenu.destroy()


    def __init__(self, master: tk.Tk) -> None:
        
        # Creacion del contenedor de los objetos de la ventana.

        self.master = master
        self.mainMenu = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.mainMenu.update_idletasks()
        self.mainMenu.place(x=0, y=0)
        self.background_img = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"GuestSessionBack.png"), master=self.mainMenu) 
        self.background = self.mainMenu.create_image(512, 384, image=self.background_img)

        self.currentWidgetMaster = tk.Canvas(master = self.mainMenu, width=0, height=0)
        self.currentWidgetMaster.place(x = 250, y = 10)
        self.currentWidget = None
        
        # Creacion de cuadro de texto en el contenedor.

        self.mainMenu.create_text(
            73.5, 41.0,
            text = "Explore",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(25.0)))

        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase StarMap.

        self.img2 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"StarMapButtonG.png"))
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
            width = 150,
            height = 30)      
        
        #--------------------------------------------------
        # Creacion de boton de para instanciar un widget de clase Map Info.

        '''self.img1 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"MapInfoButton.png"))
        self.mapInfoButton = tk.Button(
            master = self.mainMenu,
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.instance_widget,
            background= "black",
            relief = "flat")

        self.mapInfoButton.place(
            x = 25, y = 130,
            width = 150,
            height = 30)'''

        #--------------------------------------------------
        # Creacion de boton de para cerrar la sesion y volver al menu de acceso.

        self.img3 = tk.PhotoImage(file = os.path.join(GuestMenu.recursos_path,"ReturnToMenuG.png"))
        
        self.closeSessionButton = tk.Button(
            master = self.mainMenu,
            image = self.img3,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.close_session,
            background= "black",
            relief = "flat")

        self.closeSessionButton.place(
            x = 25, y = 659,
            width = 196,
            height = 42)

