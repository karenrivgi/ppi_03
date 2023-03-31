import tkinter as tk
from Widgets.StarMap import StarMap
import os

class MemberMenu:

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def __init__(self, master: tk.Tk, user = None) -> None:
        
        self.user = user
        self.widgets = []
        self.mainMenu = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.mainMenu.update_idletasks()
        self.mainMenu.place(x=0, y=0)
        self.widgets.append(self.mainMenu)

        self.background_img = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MainMenuBack.png"), master=self.mainMenu) 
        self.background = self.mainMenu.create_image(512, 384, image=self.background_img)
        
        ########################################
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

        ########################################
        self.img2 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"StarMapButton.png"))
        self.starMapButton = tk.Button(
            image = self.img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.btn_clicked(StarMap),
            background= "black",
            relief = "flat")

        self.starMapButton.place(
            x = 25, y = 80,
            width = 109,
            height = 32)        
        self.widgets.append(self.starMapButton)

        ########################################
        self.img0 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"NewsButton.png"))
        
        self.newsfeedButton = tk.Button(
            image = self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.btn_clicked,
            background= "black",
            relief = "flat")
        
        self.newsfeedButton.place(
            x = 25, y = 180,
            width = 119,
            height = 32)
        self.widgets.append(self.newsfeedButton)

        ########################################
        self.img1 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"ObjectSearchButton.png"))
        self.objectSearchButton = tk.Button(
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.btn_clicked,
            background= "black",
            relief = "flat")

        self.objectSearchButton.place(
            x = 25, y = 130,
            width = 171,
            height = 32)
        self.widgets.append(self.objectSearchButton)

        ########################################
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

        ########################################
        self.img4 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"SettingsButton.png"))
        self.settingsButton = tk.Button(
            image = self.img4,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.btn_clicked,
            background= "black",
            relief = "flat")

        self.settingsButton.place(
            x = 25, y = 559,
            width = 98,
            height = 32)
        self.widgets.append(self.settingsButton)

        ########################################
        self.img5 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"StarsButton.png"))
        self.myStarsButton = tk.Button(
            image = self.img5,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.btn_clicked,
            background= "black",
            relief = "flat")

        self.myStarsButton.place(
            x = 25, y = 509,
            width = 103,
            height = 32)
        self.widgets.append(self.myStarsButton)

        ########################################
        self.img6 = tk.PhotoImage(file = os.path.join(MemberMenu.recursos_path,"MapsButton.png"))
        self.myMapsButton = tk.Button(
            image = self.img6,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.btn_clicked,
            background= "black",
            relief = "flat")

        self.myMapsButton.place(
            x = 25, y = 459,
            width = 106,
            height = 32)    
        self.widgets.append(self.myMapsButton)   

    def btn_clicked(self, widget):
        
        canvasWidgets = tk.Canvas(master = self.mainMenu, width = 764, height = 748)
        canvasWidgets.place(x = 262, y = 20)
        canvasWidgets.update_idletasks()

        widget(master = canvasWidgets, user = self.user)

    def close_session(self):
        for wid in self.widgets:
            wid.destroy() 