import os
import shutil
import pickle

import praw
import requests
import numpy as np
import cv2

from api_reddit.create_access import create_access
from api_reddit.posts import Post


def create_folder():
    """crear las carpetas necesarias si estas no existen"""

    for folder_path in [ignore_path, image_path]:
        CHECK_FOLDER = os.path.isdir(folder_path)

        # si la carpeta no existe, entonces hay que crearla
        if not CHECK_FOLDER:
            os.makedirs(folder_path)

def delete_folders():
    """eliminar las carpetas creadas cuando no sean necesarias"""

    for folder_path in [ignore_path, image_path]:
        CHECK_FOLDER = os.path.isdir(folder_path)

        # si la carpeta existe, hay que eliminarla
        if CHECK_FOLDER:
            shutil.rmtree(folder_path)


def get_posts(POST_SEARCH_AMOUNT):
    """funcion encargada de recuperar los post en base a la cantidad especificada

        parametros:
            - POST_SEARCH_AMOUNT (int): cantidad de post a sacar por cada subreddit

        retorna:
            - posts (list): lista de los post recopilados
    """

    # crear las carpetas para guardar las imagenes de los post que tengan
    create_folder()

    # generar instancia de la API de reddit
    reddit = get_access()

    # lista para guardar los post recuperados
    posts = []

    # lista de los subreddits objetivo, recuperado del archivo "subreddit_list.cvs"
    f_final = open(os.path.join(dir_path,'subreddit_list.csv'), "r")

    # iterar sobre cada subreddit especificado en el archivo
    for line in f_final:

        sub = line.strip()

        # seleccionar subreddir por medio de la instancia de la API
        subreddit = reddit.subreddit(sub)

        count = 0

        # iterar sobre cada post obtenido del subreddit
        for submission in subreddit.hot(limit=POST_SEARCH_AMOUNT):

            # determinar si el post contiene una imagen
            if ".jpg" in submission.url.lower() or ".png" in submission.url.lower():
                try:

                    # hacer la peticion para obtener la imagen del post y tratarla por medio de openCV
                    resp = requests.get(submission.url.lower(), stream=True).raw
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                    compare_image = cv2.resize(image,(224,224))

                    # recuperar todas los paths de las imagenes presentes en la carpeta "ignore_images"
                    for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                        ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                    ignore_flag = False

                    # iterar sobre cada imagen de la carpe "ignore_images"
                    for ignore in ignore_paths:
                        
                        # leer la imagen respectiva
                        ignore = cv2.imread(ignore)

                        # obtener la diferencia entre la representación de pixeles de la imagen en la carpeta
                        # "ignore_images" y la imagen descargada por medio de la petición
                        difference = cv2.subtract(ignore, compare_image)

                        # separar los vectores de cada color
                        b, g, r = cv2.split(difference)

                        # sumar el total de valores diferentes de cero despues de hacer la diferencia
                        total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)

                        # si la diferencia total es 0, eso implica que las imagenes son las mismas, entonces ficha
                        # imagen descargada se debe ignorar al momento de guardarla
                        if total_difference == 0:
                            ignore_flag = True

                    # si la imagen no se ha guardado ya
                    if not ignore_flag:

                        # cambiar el tamaño de la imagen para mostrarla posteriormente en el newsfeed
                        image = cv2.resize(image,(300,300))

                        # guardar las imagenes en las dos carpetas
                        cv2.imwrite(f"{image_path}{sub}-{submission.id}.png", image)
                        cv2.imwrite(f"{ignore_path}{sub}-{submission.id}.png", compare_image)

                    # crear las variables necesarias para construir un objeto de un post
                    post_path = (f"{image_path}{sub}-{submission.id}.png")
                    post_header = (submission.title)
                    post_author = (submission.author.name)
                    post_body = (submission.selftext)
                    post_score = (str(submission.score))

                    # agregar a la lista de posts, el nuevo post generado con los datos
                    posts.append(Post(post_header, post_body, post_author, post_score, sub, post_path))
                        
                except Exception as e:

                    # capturar excepcion por si sucede algún error durante la ejecución
                    print(f"Image failed. {submission.url.lower()}")
                    print(e)
            
            # en el caso de que el post no tenga una imagen, crear el post sólo con los campos de texto
            else:
                post_header = (submission.title)
                post_author = (submission.author.name)
                post_body = (submission.selftext)
                post_score = (str(submission.score))
                posts.append(Post(post_header, post_body, post_author, post_score, sub))

    return posts


def get_access():
    """funcion encargada de crear la instancia de la API de reddit"""

    # verificar si ya se ha creado el token anteriormente y crearlo o recuperarlo según sea el caso
    if os.path.exists(os.path.join(dir_path,'token.pickle')):
        with open(os.path.join(dir_path,'token.pickle'), 'rb') as token:
            creds = pickle.load(token)
    else:
        creds = create_access()
        pickle_out = open(os.path.join(dir_path,'token.pickle',"wb"))
        pickle.dump(creds, pickle_out)

    # crear la instancia de la API de reddit
    reddit = praw.Reddit(client_id=creds['client_id'],
                        client_secret=creds['client_secret'],
                        user_agent=creds['user_agent'],
                        username=creds['username'],
                        password=creds['password'])
    
    # devolver la instancia de la API
    return reddit
    

# Path to save images
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "images/")
ignore_path = os.path.join(dir_path, "ignore_images/")