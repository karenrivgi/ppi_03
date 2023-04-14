import os
import pickle

import praw

from api_reddit import create_access


def make_post(user, location, date):
    """funcion encargada de hacer una publicación con la cuenta de la aplicación
    al subreddit de la aplicación, llamado "PyMansSky".

        parametros:
            - user (Usuario): usuario que hace la publicacion
            - location (str): localización sobre la que se generó el mapa estelar
            - date (str): fecha sobre la que se generó el mapa estelar

        retorna:
            - titulo (str): titulo del post generado en el subreddit
            - link (str): link en el que se aloja la publiación generada

    """

    dir_path_api = os.path.dirname(os.path.realpath(__file__))
    token_file = os.path.join(dir_path_api, "token.pickle")

    # Verificar si ya existen las credenciales para acceder a la API, y cargarla
    # o crearla si es el caso

    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    else:
        creds = create_access()
        pickle_out = open(token_file, "wb")
        pickle.dump(creds, pickle_out)

    # Generar la instancia de la API
    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret=creds['client_secret'],
                         user_agent=creds['user_agent'],
                         username=creds['username'],
                         password=creds['password'])

    # Guardar la dirección de la imagen a subir
    dir_path = os.getcwd()
    map_path = os.path.join(dir_path, "map.png")

    # Seleccionar el subreddit de la aplicación
    sub = reddit.subreddit("PyMansSky")

    # Crear el titulo de la publiación
    title = f"Skymap de {user.nickname} en {location}, {date}"

    # Generar la publicación
    submition = sub.submit_image(title=title, image_path=map_path)

    # obtener el link de la publicación
    link = f"https://www.reddit.com{submition.permalink}"

    return title, link