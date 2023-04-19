import tkinter as tk
import os
from user_data.User import Usuario
from tkinter import messagebox
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class RecoverPasswordMenu:

    # Referencia al directorio con los recursos graficos.

    recursos_path = os.path.join(os.path.dirname(__file__),"Recursos")

    def returnHome(self):
        """Instancia una ventana de clase AccessMenu y destruye la ventana actual"""
        for wid in self.widgets:
            wid.destroy()

    def recover_password(self):
        """Envia el dato de contraseña al correo electronico del usuario en caso
        de ser solicitada"""

        # Configuracion e inicializacion del srvidor SMTP

        sender_email = "ppi_project@outlook.com"
        sender_password = "ppi_123_4545"

        smtp_server = "smtp.office365.com"
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)


        server.starttls()
        server.login(sender_email, sender_password)

        # Tomar los valores de las entradas y encontrar el usuario correspondiente
        nick = self.nicknameEntry.get()
        user = None
        
        try:
            user = Usuario.leer_usuarios().get(nick)
        except:
             pass
        
        if user == None:
            
            messagebox.showwarning("Warning", "Please enter a valid user nickname.")
            return
        
        user_email = user.email
        email_entry = self.emailEntry.get()

        if user_email != email_entry:

            messagebox.showwarning("Warning", "The submited Email does not correspond with user's Email.")
            return
        
        else:
            print("ENTRAMOS xd")
            # Construccion y envio del mensaje a traves del email remitente
            mensaje = MIMEMultipart()

            mensaje['From'] = sender_email
            mensaje['To'] = user_email
            mensaje['Subject'] = "PyMan's Sky Password Recover"

            cuerpo_mensaje = f"Greetings {nick}. \n\n Your account password is: {user.contrasena}"
            mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

            # Enviar mensaje
            server.sendmail(sender_email, user_email, mensaje.as_string())

            # Cerrar conexión
            server.quit()


    def __init__(self, master: tk.Tk) -> None:

            # Creacion del contenedor de los objetos de la ventana.

            self.widgets = []
            self.master = master
            self.recover = tk.Canvas(master, width= master.winfo_width(), height= master.winfo_height(),bd = 0, highlightthickness = 0, relief = "ridge", bg="black")
            self.recover.update_idletasks()
            self.recover.place(x=0, y=0)
            self.widgets.append(self.recover)
            self.background_img = tk.PhotoImage(file = os.path.join(RecoverPasswordMenu.recursos_path,"RecoverBackground.png"), master=self.recover) 
            self.background = self.recover.create_image(512, 384, image=self.background_img)

            #--------------------------------------------------
            # Creacion de boton de para registrar un nuevo usuario.

            self.imgSignUp = tk.PhotoImage(file = os.path.join(RecoverPasswordMenu.recursos_path,"SignUpButton.png"))
            self.registerButton = tk.Button(
                image=self.imgSignUp,
                borderwidth = 0,
                command = lambda: self.recover_password(),
                highlightthickness = 0,
                relief = "flat")

            self.registerButton.place(
                x = 251, y = 500,
                width = 248,
                height = 54)
            self.widgets.append(self.registerButton)

            #--------------------------------------------------
            # Creacion de boton de para regresar al menu de acceso.

            self.imgReturn = tk.PhotoImage(file = os.path.join(RecoverPasswordMenu.recursos_path,"ReturnToMenuButton.png"))
            self.returnButton = tk.Button(
                image=self.imgReturn,
                borderwidth = 0,
                command = self.returnHome,
                highlightthickness = 0,
                relief = "flat")

            self.returnButton.place(
                x = 555, y = 500,
                width = 248,
                height = 54)
            self.widgets.append(self.returnButton)

            #--------------------------------------------------
            # Creacion de entradas de texto de nombre, correo, contraseña y confirmacion de contraseña.
            
            self.nicknameEntry = tk.Entry(
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0,
                font=("BeVietnamPro 20"))

            self.nicknameEntry.place(
                x = 370, y = 270,
                width = 350,
                height = 38,)
            self.widgets.append(self.nicknameEntry)

            self.emailEntry = tk.Entry(
                bd = 0,
                bg = "#ffffff",
                highlightthickness = 0,
                font=("BeVietnamPro 20"))

            self.emailEntry.place(
                x = 370, y = 376,
                width = 350,
                height = 38)
            self.widgets.append(self.emailEntry)