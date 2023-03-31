import tkinter as tk
from GuestMenu import GuestMenu
from MemberMenu import MemberMenu
from user_data.User import Usuario
import os
from tkinter import messagebox
from CreateAccount import CreateAccount

class AccessMenu:

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def btn_clicked(self):
        print("Button Clicked")

    def login(self):
        nickname = self.nameEntry.get()
        password = self.passwordEntry.get()

        self.nameEntry.delete(0, tk.END)
        self.passwordEntry.delete(0, tk.END)

        if not nickname or not password:
            messagebox.showwarning("Warning", "Please enter the requested data to login.")
            return
        
        user = Usuario.login(nickname, password)
        if not user:
            messagebox.showerror("Error", "Incorrect nickname or password")
            return
        
        MemberMenu(master= self.master, user = user)

    def create_account(self):
        CreateAccount(master=self.master)

    def guestAccess(self):
        GuestMenu(master= self.master)

    def __init__(self, master: tk.Tk) -> None:

        self.master = master
        self.access = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.access.update_idletasks()
        self.access.place(x=0, y=0)

        self.background_img = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"AccessBack.png"), master=self.access) 
        self.background = self.access.create_image(512, 384, image=self.background_img)

        self.access.create_text(
            512.5, 315.5,
            text = "Log into your account",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(40.0)))

        ########################################
        self.img0 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"GuestButton.png"), master=self.access)

        self.guestButton = tk.Button(
            image= self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.guestAccess(),
            background= "black",
            relief = "flat")
        
        self.guestButton.place(
            x = 596, y = 650,
            width = 117,
            height = 23)
        
        ########################################
        self.img1 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"RegisterButton.png"))

        self.createAccountButton = tk.Button(
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.create_account,
            background= "black",
            relief = "flat")

        self.createAccountButton.place(
            x = 312, y = 650,
            width = 160,
            height = 23)

        ########################################
        self.img2 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"LoginButton.png"))
        
        self.loginButton = tk.Button(
            image = self.img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.login,
            background= "black",
            relief = "flat")

        self.loginButton.place(
            x = 362, y = 580,
            width = 300,
            height = 40)
        
        ########################################
        self.nameEntry = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            font=("BeVietnamPro 20"))

        self.nameEntry.place(
            x = 362, y = 400,
            width = 350,
            height = 38,)

        ########################################
        self.passwordEntry = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            font=("BeVietnamPro 20"),
            show="*")

        self.passwordEntry.place(
            x = 362, y = 480,
            width = 350,
            height = 38)



window = tk.Tk()
window.geometry("1024x768")
window.update_idletasks()
AccessMenu(window)
window.mainloop()