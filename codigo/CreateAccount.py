import tkinter as tk
import os
from user_data.User import Usuario
from tkinter import messagebox
import re
import validate_email


class CreateAccount:
    '''
    Clase "CreateAccount" que contiene la variable que referencia al directorio
    con los recursos gráficos, también contiene las funciones:
    - returnHome()
    - register()
    - __init__()
    '''

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__), "Recursos")

    def returnHome(self):
        """
        Instancia una ventana de clase AccessMenu y destruye la ventana actual

        Parámetros: 
        - self.
        """
        for wid in self.widgets:
            wid.destroy()

    def register(self):
        """
        Obtiene la informacion ingresada en las entradas de texto e instancia
        un objeto de clase User con los datos de nickname y password.

        Parámetros:
        - self.
        """

        # Variable que almacena el valor ingresado en nicknameEntry.
        nickname = self.nicknameEntry.get()
        # Variable que almacena el valor ingresado en passwordEntry.
        password = self.passwordEntry.get()
        # Variable que almacena el valor ingresado en passwordEntry2.
        passwordConfirmation = self.passwordEntry2.get()
        # Variable que almacena el valor ingresado en emailEntry2.
        email = self.emailEntry2.get()

        # Excepciones para el nombre de la cuenta.
        nick_regex = r'^[a-zA-Z0-9]{8,}$'
        # Excepciones para la contraseña de la cuenta.
        password_regex = r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9]{8,}$'

        # Elimina lo ingresado en nicknameEmtry.
        self.nicknameEntry.delete(0, tk.END)
        # Elimina lo ingresado en passwordEmtry.
        self.passwordEntry.delete(0, tk.END)
        # Elimina lo ingresado en passwordEmtry2.
        self.passwordEntry2.delete(0, tk.END)

        # Verificaciones de existencia y validez de los datos suministrados para las cuentas.
        # Uso de Regex para comprobar la calidad de los datos para generar cuentas mas seguras.

        # If que verifica si el nombre es válido, si no lo es, muestra un "Warning" en la interfaz.
        if not nickname or re.search(nick_regex, nickname) == None:
            messagebox.showwarning("Warning", "Please enter a valid nickname.")
            return

        # If que verifica si la contraseña es válida, si no lo es, muestra un "Warning" en la interfaz.
        if not password or re.search(password_regex, password) == None:

            messagebox.showwarning("Warning", "Please enter a valid password.")
            return

        # If que verifica si la contraseña es igual a la ingresada en confirmar contraseña,
        # si no lo es, muestra un "Warning" en la interfaz.
        if password != passwordConfirmation:
            messagebox.showwarning(
                "Warning", "Password confirmation is not equal to the original password.")
            return

        # If que verifica si el email es válido, si no lo es, muestra un "Warning" en la interfaz.
        if validate_email.validate_email(email) != True:
            messagebox.showwarning("Warning", "Please enter a valid Email.")
            return

        # Asigna el usuario llamando al metodo registrar_usuario de User.py.
        new_user = Usuario.registrar_usuario(nickname, email, password)

        # If que verifica si es un usuario nuevo si no lo es, muestra un "Warning" en la interfaz.
        # Si lo es, muestra una ventana emergente confirmando la creación de la cuenta.
        if not new_user:
            messagebox.showwarning(
                "Warning", "The nickname is already being used.")
            return
        else:
            messagebox.showinfo("Confirmation", "Account created successfully")
            self.returnHome()

    def __init__(self, master: tk.Tk) -> None:
        '''
        Esta función crea una ventana gráfica para la clase CreateAccount, donde se encuentran el contenedor
        principal que incluye dentro de este un cuadro de texto, cuatro entradas de texto para:
        nombre, correo, contraseña y confirmación de contraseña, dos botones:
        - "returnButton" para llamar a la función returnHome
        - "registerButton" para llamar la función register.
        Y un cuadro de ventana emergente para restricciones nombre y constraseña.
        '''

        # Creacion del contenedor principal para los objetos de la ventana.

        self.widgets = []  # Lista que almacena objetos.
        self.master = master  # Asigna a la variable master el valor master.
        self.create_account = tk.Canvas(master, width=master.winfo_width(), height=master.winfo_height(
        ), bd=0, highlightthickness=0, relief="ridge", bg="black")  # Crea contenedor principal tipo Canvas.
        self.create_account.update_idletasks() # Forza la actualización del widget "recover".
        self.create_account.place(x=0, y=0)  # Posiciona el widget "recover".
        self.widgets.append(self.create_account) # Se agrega el widget "recover" a la lista "widgets".

        # Creación variable "background_img" que almacena la imagen "CreateAccount.png".
        self.background_img = tk.PhotoImage(file=os.path.join(
            CreateAccount.recursos_path, "CreateAccount.png"), master=self.create_account)
        
        # Creación variable que almacena el contenedor agregandole el fondo de la variable "backgroun_img".
        self.background = self.create_account.create_image(
            512, 384, image=self.background_img)

        # Creacion de cuadro de texto en el contenedor.

        self.create_account.create_text(
            515, 200,
            text="Fill the entries with the requested information",
            fill="#ffffff",
            font=("BeVietnamPro-Bold", int(28.0)))

        # --------------------------------------------------
        # Creacion de boton de para registrar un nuevo usuario.

        # Asigna la imagen "SignUpButton.png" a la variable "imgSignUp".
        self.imgSignUp = tk.PhotoImage(file=os.path.join(
            CreateAccount.recursos_path, "SignUpButton.png"))
        
        self.registerButton = tk.Button(
            image=self.imgSignUp,
            borderwidth=0,
            command=self.register,
            highlightthickness=0,
            relief="flat")  # Creación del botón que llama a la funcion "register()".
        self.registerButton.place(
            x=251, y=670,
            width=248,
            height=54) # Posicionamiento del Botón en el contenedor principal.
        self.widgets.append(self.registerButton) # Agrega el botón a la lista widgets.

        # --------------------------------------------------
        # Creacion de boton de para regresar al menu de acceso.

        # Asigna la imagen "ReturnToMenuButton.png" a la variable "imgReturn".
        self.imgReturn = tk.PhotoImage(file=os.path.join(
            CreateAccount.recursos_path, "ReturnToMenuButton.png"))
        self.returnButton = tk.Button(
            image=self.imgReturn,
            borderwidth=0,
            command=self.returnHome,
            highlightthickness=0,
            relief="flat")  # Creación del botón que llama a la funcion "returnHome()".
        self.returnButton.place(
            x=555, y=670,
            width=248,
            height=54) # Posicionamiento del Botón en el contenedor principal.
        self.widgets.append(self.returnButton) # Agrega el botón a la lista widgets.

        # --------------------------------------------------
        # Creacion de entradas de texto de nombre, correo, contraseña y confirmacion de contraseña.

        self.nicknameEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"))  # Entrada de texto para nombre.
        self.nicknameEntry.place(
            x=370, y=270,
            width=350,
            height=38,) # Posicionamiento entrada de texto nombre.
        self.widgets.append(self.nicknameEntry) # Agrega la entrada de texto a la lista widgets.

        self.emailEntry2 = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"))  # Entrada de texto para correo.
        self.emailEntry2.place(
            x=370, y=376,
            width=350,
            height=38) # Posicionamiento entrada de texto correo.
        self.widgets.append(self.emailEntry2) # Agrega la entrada de texto a la lista widgets.s

        self.passwordEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"),
            show="*")  # Entrada de texto para contraseña.
        self.passwordEntry.place(
            x=370, y=478,
            width=350,
            height=38) # Posicionamiento entrada de texto contraseña.
        self.widgets.append(self.passwordEntry) # Agrega la entrada de texto a la lista widgets.

        self.passwordEntry2 = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"),
            show="*")  # Entrada de texto para confirmar contraseña.
        self.passwordEntry2.place(
            x=370, y=585,
            width=350,
            height=38)  # Posicionamiento entrada de texto confirmar contraseña
        self.widgets.append(self.passwordEntry2) # Agrega la entrada de texto a la lista widgets.

        # Cuadro de ventana emergente para restricciones Nombre y Constraseña.
        info = ["Nickname: Must be at least 8 characters, can be numbers or letters.",
                "Password: Must have at least 8 characters, at least one capital letter and one digit. No special characters."]
        messagebox.showinfo(
            "Requirements to create an account", "\n".join(info))
