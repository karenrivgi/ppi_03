import stdiomask

def create_access():
    """funcion encargada de obtener las credenciales por consola cuando 
    se quiera generar un nuevo token dde acceso a la API

        retorna:
            - creds (dict): diccionario con las credenciales necesarias
    """

    creds = {}
    creds['client_id'] = input('client_id: ')
    creds['client_secret'] = stdiomask.getpass(prompt="client_secret: ")
    creds['user_agent'] = input('user_agent: ')
    creds['username'] = input('username: ')
    creds['password'] = stdiomask.getpass()
    return creds