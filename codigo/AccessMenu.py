import tkinter as tk
import os
from GuestMenu import GuestMenu
from CreateAccount import CreateAccount
from MemberMenu import MemberMenu
from RecoverPasswordMenu import RecoverPasswordMenu
from user_data.User import Usuario  
from tkinter import messagebox
from api_reddit.get_posts_data import delete_folders

class AccessMenu:

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def login(self):
        """Recopila los datos ingresados en los campos de entrada de
        nickname y password; y los compara con los datos de las cuentas
        registradas para dar acceso al menu de usuarios registrados con
        la cuenta ingresada."""

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
        
        #Verificación del guardado de los historiales mientras se implementa en la interfaz:
        #print(user.historial)
        #print(user.historial_reddit)
        
        MemberMenu(master= self.master, user = user)


    def create_account(self):
        
        """Instancia una ventana de clase CreateAccount."""
        CreateAccount(master=self.master)


    def recover_account(self):
        
        """Instancia una ventana de clase CreateAccount."""
        RecoverPasswordMenu(master=self.master)


    def guestAccess(self):
        """Instancia una ventana de clase GuestMenu."""
        GuestMenu(master= self.master)


    def __init__(self, master: tk.Tk) -> None:

        # Elimina las imagenes de los post de reddir, si por alguna razón ya existen algunas
        delete_folders()

        # Creacion del contenedor de los objetos de la ventana.

        self.master = master
        self.access = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
        self.access.update_idletasks()
        self.access.place(x=0, y=0)
        self.background_img = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"AccessBack.png"), master=self.access) 
        self.background = self.access.create_image(512, 384, image=self.background_img)

        # Creacion de cuadro de texto en el contenedor.

        self.access.create_text(
            512.5, 315.5,
            text = "Log into your account",
            fill = "#ffffff",
            font = ("BeVietnamPro-Bold", int(40.0)))

        #--------------------------------------------------
        # Creacion de boton de acceso al menu de invitados.

        self.img0 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"GuestButton.png"), master=self.access)

        self.guestButton = tk.Button(
            image= self.img0,
            borderwidth = 0,
            highlightthickness = 0,
            command = lambda: self.guestAccess(),
            background= "black",
            relief = "flat")
        
        self.guestButton.place(
            x = 606, y = 670,
            width = 180,
            height = 23)
        
        #--------------------------------------------------
        # Creacion del boton de acceso al menu de creacion de cuentas.

        self.img1 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"RegisterButton.png"))

        self.createAccountButton = tk.Button(
            image = self.img1,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.create_account,
            background= "black",
            relief = "flat")

        self.createAccountButton.place(
            x = 282, y = 670,
            width = 180,
            height = 23)

        #--------------------------------------------------
        # Creacion del boton para carga de datos del login y acceso al menu de usuarios registrados.

        self.img2 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"LoginButton.png"))
        
        self.loginButton = tk.Button(
            image = self.img2,
            borderwidth = 0,
            highlightthickness = 0,
            command = self.login,
            background= "black",
            relief = "flat")

        self.loginButton.place(
            x = 374, y = 580,
            width = 300,
            height = 40)
        
        #--------------------------------------------------
        # Creacion del boton para opción de recuperar la cuenta si se olvidó la contraseña.

        self.img3 = tk.PhotoImage(file = os.path.join(AccessMenu.recursos_path,"ForgotPasswordButton.png"))
        
        self.forgotPasswordButton = tk.Button(
            image = self.img3,
            borderwidth = 0,
            highlightthickness = 0,
            command= lambda: self.recover_account(),
            relief = "flat")

        self.forgotPasswordButton.place(
            x = 444, y = 630,
            width = 164,
            height = 20)

        #--------------------------------------------------
        # Creacion de cuadros de texto para ingresar nombre de usuario y contraseña.

        self.nameEntry = tk.Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            font=("BeVietnamPro 20"))

        self.nameEntry.place(
            x = 362, y = 400,
            width = 350,
            height = 38,)

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
window.resizable(True, True)
window.title("Py Man's Sky")
window.update_idletasks()
AccessMenu(window)
window.mainloop()