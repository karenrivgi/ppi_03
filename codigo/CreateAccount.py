import tkinter as tk
import os
from user_data.User import Usuario
from tkinter import messagebox

class CreateAccount:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def returnHome(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""
        for wid in self.widgets:
            wid.destroy()


    def register(self):
        """Obtiene la informacion ingresada en las entradas de texto e instancia
        un objeto de clase User con los datos de nickname y password."""

        nickname = self.nicknameEntry.get()
        password = self.passwordEntry.get()
        passwordConfirmation = self.passwordEntry2.get()

        self.nicknameEntry.delete(0, tk.END)
        self.passwordEntry.delete(0, tk.END)
        self.passwordEntry2.delete(0, tk.END)


        if not nickname:
            messagebox.showwarning("Warning", "Please enter a nickname.")
            return

        if password != passwordConfirmation:
            messagebox.showwarning("Warning", "Password confirmation is not equal to the original password.")
            return
        
        new_user = Usuario.registrar_usuario(nickname, password)

        if not new_user:
            messagebox.showwarning("Warning", "The nickname is already being used.")
            return
        else:
            messagebox.showinfo("Confirmation", "Account created successfully")
            self.returnHome()
             

    def __init__(self, master: tk.Tk) -> None:

            # Creacion del contenedor de los objetos de la ventana.

            self.widgets = []
            self.master = master
            self.create_account = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
            self.create_account.update_idletasks()
            self.create_account.place(x=0, y=0)
            self.widgets.append(self.create_account)
            self.background_img = tk.PhotoImage(file = os.path.join(CreateAccount.recursos_path,"Create account.png"), master=self.create_account) 
            self.background = self.create_account.create_image(512, 384, image=self.background_img)

            # Creacion de cuadro de texto en el contenedor.

            self.create_account.create_text(
                512.5, 200,
                text = "Fill the entries with the requested information",
                fill = "#ffffff",
                font = ("BeVietnamPro-Bold", int(30.0)))
            
            #--------------------------------------------------
            # Creacion de boton de para registrar un nuevo usuario.

            self.imgSignUp = tk.PhotoImage(file = os.path.join(CreateAccount.recursos_path,"SignUpButton.png"))
            self.registerButton = tk.Button(
                image=self.imgSignUp,
                borderwidth = 0,
                command = self.register,
                highlightthickness = 0,
                relief = "flat")

            self.registerButton.place(
                x = 251, y = 597,
                width = 248,
                height = 54)
            self.widgets.append(self.registerButton)

            #--------------------------------------------------
            # Creacion de boton de para regresar al menu de acceso.

            self.imgReturn = tk.PhotoImage(file = os.path.join(CreateAccount.recursos_path,"ReturnButton.png"))
            self.returnButton = tk.Button(
                image=self.imgReturn,
                borderwidth = 0,
                command = self.returnHome,
                highlightthickness = 0,
                relief = "flat")

            self.returnButton.place(
                x = 555, y = 597,
                width = 248,
                height = 54)
            self.widgets.append(self.returnButton)

            #--------------------------------------------------
            # Creacion de entradas de texto de nombre, contraseña y confirmacion de contraseña.
            
            self.nicknameEntry = tk.Entry(
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0,
                font=("BeVietnamPro 20"))

            self.nicknameEntry.place(
                x = 370, y = 287,
                width = 350,
                height = 38,)
            self.widgets.append(self.nicknameEntry)

            self.passwordEntry = tk.Entry(
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0,
                font=("BeVietnamPro 20"),
                show="*")

            self.passwordEntry.place(
                x = 370, y = 400,
                width = 350,
                height = 38)
            self.widgets.append(self.passwordEntry)

            self.passwordEntry2 = tk.Entry(
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0,
                font=("BeVietnamPro 20"),
                show="*")

            self.passwordEntry2.place(
                x = 370, y = 523,
                width = 350,
                height = 38)
            self.widgets.append(self.passwordEntry2)
