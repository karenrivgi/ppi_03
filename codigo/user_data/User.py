import pickle
import os


class Usuario:

    # Define la ruta absoluta del directorio donde se encuentra el archivo de
    # datos.
    DATA_PATH = os.path.abspath(os.path.dirname(__file__))

    # Constructor de la clase Usuario.
    def __init__(
            self,
            nickname,
            email,
            contrasena,
            historial=None,
            historial_reddit=None,
            historial_astros=None):
        # Inicializa los atributos nickname, contrasena y historial del objeto.
        self.nickname = nickname
        self.email = email
        self.contrasena = contrasena
        self.historial = historial or []
        # self.historial_reddit = historial_reddit or []
        self.historial_astros = historial_astros or []

    @classmethod
    def registrar_usuario(cls, nickname, email, contrasena):
        """ Registra un nuevo usuario en el sistema.

        Args:
            nickname (str): El nombre de usuario deseado.
            email (str): La dirección de correo electrónico del usuario.
            contrasena (str): La contraseña elegida por el usuario.

        Returns:
            bool: True si se registró el usuario correctamente, False si el nickname ya está en uso.
        """

        # Lee los usuarios existentes del archivo de datos.
        usuarios = cls.leer_usuarios()

        # Si el nickname ya existe, retorna False
        if nickname in usuarios:
            return False

         # Si el nickname no existe, crea un objeto Usuario con el nickname y
         # la contraseña, y lo guarda en el archivo pickle
        with open(os.path.join(Usuario.DATA_PATH, "usuarios.pickle"), "ab") as f:
            usuario = Usuario(nickname, email, contrasena)
            pickle.dump(usuario, f)

        # Si ya lo registró,  retorna True
        return True

    @classmethod
    def login(cls, nickname, contrasena):
        """ Verifica si el usuario con el nickname y la contraseña proporcionados existen en el archivo de usuarios pickle.

        Parámetros:
        - nickname (str): el nombre de usuario que se quiere autenticar.
        - contrasena (str): la contraseña del usuario que se quiere autenticar.

        Retorna:
        - (Usuario): el objeto Usuario correspondiente si las credenciales de autenticación son correctas.
        - (bool): False si el nickname no existe o la contraseña no coincide.
        """

        # Carga los usuarios existentes desde el archivo pickle
        usuarios = cls.leer_usuarios()

        if nickname not in usuarios or usuarios[nickname].contrasena != contrasena:
            # Si el nickname no existe o la contraseña no coincide, devuelve
            # False
            return False

        # Si el nickname y la contraseña coinciden, devuelve el objeto Usuario
        # correspondiente
        elif usuarios[nickname].contrasena == contrasena:
            return usuarios[nickname]

    @classmethod
    def leer_usuarios(cls):
        """ Método de clase que lee los objetos Usuario del archivo pickle y los devuelve como un diccionario.

        Returns:
        - usuarios: Un diccionario que contiene los objetos Usuario leídos del archivo pickle.
                    Si el archivo no existe, devuelve un diccionario vacío.
        """
        try:
            # Abre el archivo pickle en modo lectura binaria
            with open(os.path.join(Usuario.DATA_PATH, "usuarios.pickle"), "rb") as f:
                usuarios = {}
                while True:
                    try:
                        # Lee un objeto Usuario desde el archivo y lo agrega al
                        # diccionario de usuarios
                        usuario = pickle.load(f)
                        usuarios[usuario.nickname] = usuario
                    except EOFError:
                        break
        except FileNotFoundError:
            # Si el archivo no existe, devuelve un diccionario vacío
            usuarios = {}

        # Devuelve el diccionario de usuarios
        return usuarios

    def guardar_historial(self, datos, tipo='input'):
        """ Método para guardar el historial de búsqueda del usuario.

        Parámetros:
        - datos: datos a agregar al historial.
        - tipo: tipo de búsqueda, por defecto es 'input'. También puede ser 'reddit' o 'astros'.

        """
        # Carga los objetos del archivo pickle y actualiza el historial del
        # usuario
        usuarios = Usuario.leer_usuarios()
        usuarios[self.nickname].historial = self.historial

        if tipo == 'reddit':
            # Actualiza los datos al historial del usuario
            # self.historial_reddit.append(datos)

            # busca la entrada en el historial correspondiente al mapa generado
            # y en la entrada correspondiente al estado de reddir, actualiza la
            # info
            for entry in self.historial:
                if entry[1] == datos[0] and entry[2] == datos[1]:
                    entry[3] = datos[2]

            # Actualizar los datos del usuario en la base de datos
            usuarios[self.nickname].historial = self.historial

        elif tipo == 'astros':
            self.historial_astros.append(datos)
            usuarios[self.nickname].historial_astros = self.historial_astros
        else:
            self.historial.append(datos)
            usuarios[self.nickname].historial = self.historial

        # Guarda los objetos actualizados en el archivo pickle
        with open(os.path.join(Usuario.DATA_PATH, "usuarios.pickle"), "wb") as f:
            for usuario in usuarios.values():
                pickle.dump(usuario, f)
