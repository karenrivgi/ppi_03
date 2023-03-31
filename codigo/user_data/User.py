import pickle
import os

class Usuario:

    data_path = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, nickname, contrasena, historial = None):
        self.nickname = nickname
        self.contrasena = contrasena
        self.historial = historial or []

    @classmethod
    def registrar_usuario(cls, nickname, contrasena):
        usuarios = cls.leer_usuarios()

        if nickname in usuarios:
            return False

        with open(os.path.join(Usuario.data_path,"usuarios.pickle"), "ab") as f:
            usuario = Usuario(nickname, contrasena)
            pickle.dump(usuario, f)
        
        return True

    @classmethod
    def login(cls, nickname, contrasena):
        usuarios = cls.leer_usuarios()

        if nickname not in usuarios or usuarios[nickname].contrasena != contrasena:
            return False 
        
        elif usuarios[nickname].contrasena == contrasena:
            return usuarios[nickname]
        
    @classmethod
    def leer_usuarios(cls):
        try:
            with open(os.path.join(Usuario.data_path,"usuarios.pickle"), "rb") as f:
                usuarios = {}
                while True:
                    try:
                        usuario = pickle.load(f)
                        usuarios[usuario.nickname] = usuario
                    except EOFError:
                        break
        except FileNotFoundError:
            usuarios = {}

        return usuarios
    
    def guardar_historial(self, datos):
        self.historial.append(datos)
        # Carga los objetos del archivo pickle y actualiza el historial del usuario
        usuarios = Usuario.leer_usuarios()
        usuarios[self.nickname].historial = self.historial

        # Guarda los objetos actualizados en el archivo pickle
        with open(os.path.join(Usuario.data_path,"usuarios.pickle"), "wb") as f:
            for usuario in usuarios.values():
                pickle.dump(usuario, f)

if __name__ == '__main__': # Implementación básica - Cambio con historial
    while True:
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        # Continuar sin iniciar sesión o crear un usuario sin nombre ni contraseña y atributo bool "registrado" para manejar esto?

        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            nickname = input("Ingrese un nickname: ")
            contrasena = input("Ingrese una contraseña: ")
            Usuario.registrar_usuario(nickname, contrasena)

        elif opcion == "2":
            nickname = input("Ingrese su nickname: ")
            contrasena = input("Ingrese su contraseña: ")
            usuario = Usuario.login(nickname, contrasena)

            if usuario:
                print("Usuario recuperado")
                print("Historial del usuario: ", usuario.historial)
                # hacer algo con el usuario loggeado, por ejemplo, mostrar su historial

        elif opcion == "3":
            break

        else:
            print("Opción inválida")



