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
    '''
    Clase "AccesMenu" que contiene la variable que referencia al directorio con los recursos gráficos,
    también contiene las funciones:
    - login()
    - create_account()
    - recover_password()
    - guestAccess()
    - __init__()
    '''

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__), "Recursos")

    def login(self):
        """Recopila los datos ingresados en los campos de entrada de
        nickname y password; y los compara con los datos de las cuentas
        registradas para dar acceso al menu de usuarios registrados con
        la cuenta ingresada.

        Parámetro:
        -self.

        Return:
        Instacia una ventana de la clase MemberMenu
        """

        # Se crea variable que almacena el valor del "nameEntry" de la funcion
        # "__init__".
        nickname = self.nameEntry.get()
        # Se crea variable que almacena el valor del "passwordEntry" de la
        # funcion "__init__".
        password = self.passwordEntry.get()

        # Llamado de clase que elimina lo ingresado en el "nameEntry" una vez
        # guardado.
        self.nameEntry.delete(0, tk.END)
        # Llamado de clase que elimina lo ingresado en el "passwordEntry" una
        # vez guardado.
        self.passwordEntry.delete(0, tk.END)

        # If que verifica que si se ha ingresado los datos de nombre y contraseña en cada uno de los cuadros de textos respectivos.
        # En caso de que no, muestra en la ventana principal una ventana
        # emergente con un "Warning".

        if not nickname or not password:
            messagebox.showwarning(
                "Warning", "Please enter the requested data to login.")
            return

        # Se crea variable "user" que almacena el llamado del metodo "login" de User.py con los parametros
        # "nickname" para el nombre ingresado y "password" para la contraseña ingresada.

        user = Usuario.login(nickname, password)

        # If que verifica que si se ha ingresado los datos de nombre y contraseña correctamente.
        # En caso de que no, muestra en la ventana principal una ventana
        # emergente con un "Error".

        if not user:
            messagebox.showerror("Error", "Incorrect nickname or password")
            return

        # Verificación del guardado de los historiales mientras se implementa en la interfaz:
        # print(user.historial)
        # print(user.historial_reddit)

        # Instacia una ventana de la clase MemberMenu.
        MemberMenu(master=self.master, user=user)

    def create_account(self):
        """
        Instancia una ventana de clase CreateAccount.

        Parámetro:
        - self
        """

        CreateAccount(master=self.master)

    def recover_account(self):
        """
        Instancia una ventana de clase RecoverPasswordMenu.

        Parámetro:
        - self
        """

        RecoverPasswordMenu(master=self.master)

    def guestAccess(self):
        """
        Instancia una ventana de clase GuestMenu.

        Parámetro:
        - self
        """

        GuestMenu(master=self.master)

    def __init__(self, master: tk.Tk) -> None:
        '''
        Esta función crea una ventana gráfica para la clase AccessMenu, contiene una función
        que elimina imagenes del post de reddit, al igual que se encuentra el contenedor
        principal, que incluye dentro de este: cuadro de texto "Log into your account", cuatro botones:
        - "guestButton" que llama la funcion guestAccess.
        - "createAccountButton" que llama la funcion create_account.
        - "loginButton" que llama la funcion login.
        - "forgotPasswordButton" que llama la funcion recover_account.
        Por último contiene los cuadros de texto para ingresar nombre y contraseña.

        Parametros:
        - self
        - master
        '''

        # Elimina las imagenes de los post de reddit, si por alguna razón ya
        # existen algunas.
        delete_folders()

        self.master = master  # Se crea variable "master" con atributo master.

        # Creacion del contenedor principal "access" tipo Canvas, para los
        # objetos de la ventana.
        self.access = tk.Canvas(
            master,
            width=master.winfo_width(),
            height=master.winfo_height(),
            bd=0,
            highlightthickness=0,
            relief="ridge",
            bg="black")

        # Se llama al metodo "update_idletasks" para forzar la actualización de
        # la interfaz.
        self.access.update_idletasks()

        self.access.place(x=0, y=0)  # Se posicióna el contenedor principal

        # Se crea variable background que contiene una clase tk.PhotoImage que
        # asigna la imagen "AcessBack.png" a la variable.
        self.background_img = tk.PhotoImage(file=os.path.join(
            AccessMenu.recursos_path, "AccessBack.png"), master=self.access)

        # Asigna la imagen de la variable background_img al contenedor "acess".
        self.background = self.access.create_image(
            512, 384, image=self.background_img)

        # Creacion de cuadro de texto en el contenedor.
        self.access.create_text(
            512.5, 315.5,
            text="Log into your account",
            fill="#ffffff",
            font=("BeVietnamPro-Bold", int(40.0)))

        # --------------------------------------------------
        # Creacion de boton de acceso al menu de invitados.

        # Asigna la imagen "GuestButton.png" a la variable "img0".
        self.img0 = tk.PhotoImage(file=os.path.join(
            AccessMenu.recursos_path, "GuestButton.png"), master=self.access)
        self.guestButton = tk.Button(
            image=self.img0,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.guestAccess(),
            background="black",
            relief="flat")  # Creación del botón que llama a la funcion "guestAcces()".
        self.guestButton.place(
            x=606, y=670,
            width=180,
            height=23)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion del boton de acceso al menu de creacion de cuentas.

        # Asigna la imagen "RegisterButton.png" a la variable "img1".
        self.img1 = tk.PhotoImage(file=os.path.join(
            AccessMenu.recursos_path, "RegisterButton.png"))
        self.createAccountButton = tk.Button(
            image=self.img1,
            borderwidth=0,
            highlightthickness=0,
            command=self.create_account,
            background="black",
            relief="flat")  # Creación del botón que llama a la función "create_account()".
        self.createAccountButton.place(
            x=282, y=670,
            width=180,
            height=23)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion del boton para carga de datos del login y acceso al menu de
        # usuarios registrados.

        # Asigna la imagen "LoginButton.png" a la variable "img2".
        self.img2 = tk.PhotoImage(file=os.path.join(
            AccessMenu.recursos_path, "LoginButton.png"))
        self.loginButton = tk.Button(
            image=self.img2,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,
            background="black",
            relief="flat")  # Creación del botón que llama a la función "login()".
        self.loginButton.place(
            x=374, y=580,
            width=300,
            height=40)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion del boton para opción de recuperar la cuenta si se olvidó la
        # contraseña.

        # Asigna la imagen "ForgotPasswordButton.png" a la variable "img3".
        self.img3 = tk.PhotoImage(file=os.path.join(
            AccessMenu.recursos_path, "ForgotPasswordButton.png"))
        self.forgotPasswordButton = tk.Button(
            image=self.img3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.recover_account(),
            relief="flat")  # Creación del botón que llama a la función "recover_account()".
        self.forgotPasswordButton.place(
            x=444, y=630,
            width=164,
            height=20)  # Posicionamiento del Botón en el contenedor principal.

        # --------------------------------------------------
        # Creacion de cuadros de texto para ingresar nombre de usuario y
        # contraseña.

        self.nameEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"))  # Creación cuadro de entrada de texto para nombre de usuario.
        self.nameEntry.place(
            x=362, y=400,
            width=350,
            height=38,)  # Posicionamiento cuadro de texto nombre de usuario.

        self.passwordEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"),
            show="*")  # Creación cuadro de entrada de texto para contraseña.
        self.passwordEntry.place(
            x=362, y=480,
            width=350,
            height=38)  # Posicionamiento cuadro de texto contraseña.


# Creación de la ventana principal de la aplicación.
window = tk.Tk()  # Crea la ventana principal.
# Asigna tamaño de la ventana principal, 1024 de ancho x 768 de alto.
window.geometry("1024x768")
# Activa la redimensionamiento de la ventana por parte del usuario.
window.resizable(True, True)
window.title("Py Man's Sky")  # Asigna nombre a la ventana principal.
window.update_idletasks()  # Forza la actualización de la ventana principal.

AccessMenu(window)  # La variable "window" inicia la clase "AccessMenu"

window.mainloop()  # Inicia el búcle y muestra la ventana principal.
