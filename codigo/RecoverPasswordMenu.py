import os
import pickle
import smtplib
import tkinter as tk
from user_data.User import Usuario
from tkinter import messagebox
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class RecoverPasswordMenu:
    '''
    Clase "RecoverPasswordMenu" que contiene la variable que referencia al directorio
    con los recursos gráficos, también contiene las funciones:
    - returnHome()
    - recover_password()
    - __init__()
    '''

    # Referencia al directorio con los recursos graficos.
    recursos_path = os.path.join(os.path.dirname(__file__), "Recursos")

    def returnHome(self):
        """
        Instancia una ventana de clase AccessMenu y destruye la ventana actual.

        Parámetro:
        - self.
        """
        for wid in self.widgets:
            wid.destroy()

    def recover_password(self):
        """
        Envia el dato de contraseña al correo electronico del usuario en caso
        de ser solicitada.

        Parámetro:
        - self.
        """

        # Tomar los valores de las entradas y encontrar el usuario
        # correspondiente.
        nick = self.nicknameEntry.get()

        user = None  # Variable "user" con valor inicial "None".

        # Variable "user" que almacena el metodo leer_usuarios() de User.py que
        # toma como argumento "nick".
        user = Usuario.leer_usuarios().get(nick)

        if user is None:  # If que verifica si el nombre ingresado es inválido, si lo es muestra un "Warning" en la interfaz.
            messagebox.showwarning(
                "Warning", "Please enter a valid user nickname.")
            return

        # Variable "user_email" que almacena el email del usuario desde
        # User.py.
        user_email = user.email

        # Variable "email_entry" que almacena el valor ingresado en el cuadro
        # de texto "emailEntry".
        email_entry = self.emailEntry.get()

        '''
        If que verifica si el valor de "user_email" es diferente de "email_entry, si lo es,
        muestra un "Warning" en la interfaz.
        Si no es diferente, inicia el servidor con los datos del correo de la aplicación,
        construyendo un mensaje que es enviado al usuario, por el correo ingresado por este,
        con la contraseña con la que se creo la cuenta.
        '''
        if user_email != email_entry:
            messagebox.showwarning(
                "Warning", "The submited Email does not correspond with user's Email.")
            return

        else:

            # Configuracion e inicializacion del servidor SMTP.

            # Dirección de los tokens de la cuenta sender
            data_dir = os.path.join(os.path.dirname(__file__), "user_data")
            token_file = os.path.join(data_dir, "tokenPpi.pickle")

            # Abrir el archivo y guardar su información en creds
            if os.path.exists(token_file):
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)

            # Variable que almacena el correo de la aplicación.
            sender_email = creds['email']
            # Variable que almacena la contraseña del correo de la aplicación.
            sender_password = creds['password']
            # Variable que almacena el nombre del servidor SMTP de Office 365.
            smtp_server = "smtp.office365.com"
            # Variable que almacena el valor del puerto asociado al servidor
            # SMTP.
            smtp_port = 587
            # Establece conexioncon un servidor SMTP utilizando servidor y
            # puerto especificado.
            server = smtplib.SMTP(smtp_server, smtp_port)
            # Inicia un conexion SMTP segura mediante el cifrado TLS.
            server.starttls()
            # El servirdor inicia sesión con las variables del correo y
            # contraseña.
            server.login(sender_email, sender_password)

            # Construccion y envio del mensaje a traves del email remitente.

            # Variable que almacena la clase del modulo "email.mime.multipart".
            mensaje = MIMEMultipart()
            # Establece el correo electronico del remitente (correo de la
            # aplicación).
            mensaje['From'] = sender_email
            # Establece el correo electronico del receptor (usuario).
            mensaje['To'] = user_email
            # Establece el asunto del correo a enviar.
            mensaje['Subject'] = "PyMan's Sky Password Recover"

            # Variable de texto con un mensaje que incluye, el nombre de
            # usuario y contraseña del usuario.
            cuerpo_mensaje = f"Greetings {nick}. \n\n Your account password is: {user.contrasena}"
            # Adjunta el texto de la variable "cuerpo_mensaje" como texto plano
            # "plain".
            mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

            # Envíar el mensaje.
            server.sendmail(sender_email, user_email, mensaje.as_string())

            # Cerrar conexión.
            server.quit() 

            # Notificarle al usuario el envío del correo
            messagebox.showinfo(
                "Mail sent",
                "The email with your password has been sent, please check your inbox in a few seconds.")

            # Regresar al menú principal
            self.returnHome()

    def __init__(self, master: tk.Tk) -> None:
        '''
        Esta función crea una ventana gráfica para la clase RecoverPasswordMenu, donde se
        encuentran el contenedor principal que incluye dentro de este dos entradas de texto
        para el nombre y correo del usuario que se guardan en la funcion recover_password,
        también se encuentran dos botones:
        - "returnButton" que llama la función returnHome
        - "registerButton" para llamar la función recover_password.

        Parámetros:
        - self.
        - master.
        '''

        # Creacion del contenedor principal para los objetos de la ventana.

        self.widgets = []  # Lista que almacena objetos.
        self.master = master  # Asigna a la variable master el valor master.
        self.recover = tk.Canvas(
            master,
            width=master.winfo_width(),
            height=master.winfo_height(),
            bd=0,
            highlightthickness=0,
            relief="ridge",
            bg="black")  # Crea contenedor principal tipo Canvas.
        # Forza la actualización del widget "recover".
        self.recover.update_idletasks()
        self.recover.place(x=0, y=0)  # Posiciona el widget "recover".
        # Se agrega el widget "recover" a la lista "widgets".
        self.widgets.append(self.recover)

        # Variable que almacena la imagen "RecoverBackground.png".
        self.background_img = tk.PhotoImage(
            file=os.path.join(
                RecoverPasswordMenu.recursos_path,
                "RecoverBackground.png"),
            master=self.recover)

        # Asigna el fondo con la variable "background_img" al widget "recover".
        self.background = self.recover.create_image(
            512, 384, image=self.background_img)

        # --------------------------------------------------
        # Creacion de boton de para registrar un nuevo usuario.

        # Asigna la imagen "RequestPasswordButton.png" a la variable
        # "imgSignUp".
        self.imgSignUp = tk.PhotoImage(file=os.path.join(
            RecoverPasswordMenu.recursos_path, "RequestPasswordButton.png"))
        self.registerButton = tk.Button(
            image=self.imgSignUp,
            borderwidth=0,
            command=lambda: self.recover_password(),
            highlightthickness=0,
            relief="flat")  # Creación del botón que llama a la funcion "recover_password()".
        self.registerButton.place(
            x=251, y=500,
            width=248,
            height=54)  # Posicionamiento del Botón en el contenedor principal
        # Agrega el botón a la lista widgets.
        self.widgets.append(self.registerButton)

        # --------------------------------------------------
        # Creacion de boton de para regresar al menu de acceso.

        # Asigna la imagen "ReturnToMenuButton.png" a la variable "imgReturn".
        self.imgReturn = tk.PhotoImage(file=os.path.join(
            RecoverPasswordMenu.recursos_path, "ReturnToMenuButton.png"))
        self.returnButton = tk.Button(
            image=self.imgReturn,
            borderwidth=0,
            command=self.returnHome,
            highlightthickness=0,
            relief="flat")  # Creación del botón que llama a la funcion "returnHome()".
        self.returnButton.place(
            x=555, y=500,
            width=248,
            height=54)  # Posicionamiento del Botón en el contenedor principal
        # Agrega el botón a la lista widgets.
        self.widgets.append(self.returnButton)

        # --------------------------------------------------
        # Creacion de entradas de texto para nombre y correo electronico.

        self.nicknameEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"))  # Entrada de texto nombre.
        self.nicknameEntry.place(
            x=370, y=270,
            width=350,
            height=38,)  # Posicionamiento entrada de texto.
        # Agrega la entrada de texto a la lista widgets.
        self.widgets.append(self.nicknameEntry)

        self.emailEntry = tk.Entry(
            bd=0,
            bg="#ffffff",
            highlightthickness=0,
            font=("BeVietnamPro 20"))  # Entrada de texto correo electronico.
        self.emailEntry.place(
            x=370, y=376,
            width=350,
            height=38)  # Posicionamiento entrada de texto.
        # Agrega la entrada de texto a la lista widgets.
        self.widgets.append(self.emailEntry)