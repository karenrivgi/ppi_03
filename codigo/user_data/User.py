import pickle
import os

class Usuario:

    # Define la ruta absoluta del directorio donde se encuentra el archivo de datos.
    DATA_PATH = os.path.abspath(os.path.dirname(__file__))

    # Constructor de la clase Usuario.
    def __init__(self, nickname, email, contrasena, historial = None, historial_reddit = None, historial_astros = None):
        # Inicializa los atributos nickname, contrasena y historial del objeto.
        self.nickname = nickname
        self.email = email
        self.contrasena = contrasena
        self.historial = historial or []
        self.historial_reddit = historial_reddit or []
        self.historial_astros = historial_astros or []
    
    @classmethod
    def registrar_usuario(cls, nickname, email, contrasena):
        # Lee los usuarios existentes del archivo de datos.
        usuarios = cls.leer_usuarios()

        # Si el nickname ya existe, retorna False
        if nickname in usuarios:
            return False

         # Si el nickname no existe, crea un objeto Usuario con el nickname y la contraseña, y lo guarda en el archivo pickle
        with open(os.path.join(Usuario.DATA_PATH,"usuarios.pickle"), "ab") as f:
            usuario = Usuario(nickname, email, contrasena)
            pickle.dump(usuario, f)

        # Si ya lo registró,  retorna True
        return True
    
    @classmethod
    def login(cls, nickname, contrasena):
        # Carga los usuarios existentes desde el archivo pickle
        usuarios = cls.leer_usuarios()

        if nickname not in usuarios or usuarios[nickname].contrasena != contrasena:
            # Si el nickname no existe o la contraseña no coincide, devuelve False
            return False 
        
        # Si el nickname y la contraseña coinciden, devuelve el objeto Usuario correspondiente
        elif usuarios[nickname].contrasena == contrasena:
            return usuarios[nickname]
    
    @classmethod
    def leer_usuarios(cls) -> dict:
        try:
            # Abre el archivo pickle en modo lectura binaria
            with open(os.path.join(Usuario.DATA_PATH,"usuarios.pickle"), "rb") as f:
                usuarios = {}
                while True:
                    try:
                        # Lee un objeto Usuario desde el archivo y lo agrega al diccionario de usuarios
                        usuario = pickle.load(f)
                        usuarios[usuario.nickname] = usuario
                    except EOFError:
                        break
        except FileNotFoundError:
            # Si el archivo no existe, devuelve un diccionario vacío
            usuarios = {}

        # Devuelve el diccionario de usuarios
        return usuarios

    def guardar_historial(self, datos, tipo = 'input'):
    
        # Carga los objetos del archivo pickle y actualiza el historial del usuario
        usuarios = Usuario.leer_usuarios()
        usuarios[self.nickname].historial = self.historial

        if tipo == 'reddit':
            # Agrega los datos al historial del usuario
            self.historial_reddit.append(datos)
            # Actualizar los datos del usuario en la base de datos
            usuarios[self.nickname].historial_reddit = self.historial_reddit
        elif tipo == 'astros':
            self.historial_astros.append(datos)
            usuarios[self.nickname].historial_astros = self.historial_astros 
        else: 
            self.historial.append(datos)
            usuarios[self.nickname].historial = self.historial

        # Guarda los objetos actualizados en el archivo pickle
        with open(os.path.join(Usuario.DATA_PATH,"usuarios.pickle"), "wb") as f:
            for usuario in usuarios.values():
                pickle.dump(usuario, f)