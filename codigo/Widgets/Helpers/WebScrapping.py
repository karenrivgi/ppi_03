import os
import tkinter as tk

import requests
import pandas as pd
import html2text

from os.path import abspath, dirname, join
from tkhtmlview import HTMLLabel
from bs4 import BeautifulSoup


def object_search(astro_type, astro):
    '''Realiza una búsqueda de un objeto astronómico (planeta o estrella) y
    devuelve información detallada sobre el objeto en forma de contenido HTML
    haciendo web scrapping.

    Args:
    - astro_type (str): Tipo de objeto astronómico a buscar, puede ser "planet"
      o cualquier otro valor que se interpreta como "estrella".
    - astro (str): Nombre común del objeto astronómico a buscar. Si astro_type
      es "planet", entonces astro debe ser el nombre del planeta. Si astro_type
      es cualquier otro valor, astro debe ser el nombre común de la estrella.

    Returns:
    - contenido_html (str): Contenido HTML con información detallada sobre el
      objeto astronómico.

    '''

    # CONSTRUCCION DE URLS

    # Si el tipo de astro es 'planet', se construye la URL con el nombre del
    # planeta.
    if astro_type == 'planet':
        url = f"https://www.universeguide.com/{astro_type}/{astro}"

    # Si el tipo de astro es 'star'
    else:

        # Se lee el archivo de nombres (names.csv), que contiene los nombres
        # comunes y los identificadores de la estrella.
        names_path = join(
            join(
                dirname(
                    dirname(
                        dirname(
                            abspath(__file__)))),
                'StarMapGenerator'),
            "names.csv")
        names = pd.read_csv(names_path)

        # Se busca el identificador de la estrella a partir del nombre común.
        HIP = names.loc[names['common name'] == astro, 'HIP'].values[0]

        # Con el HIP se construye la URL para acceder a la información
        # de la estrella.
        url = f"https://www.universeguide.com/{astro_type}/{HIP}/{astro}"

    # Se hace una solicitud GET a la URL y se obtiene el contenido HTML de la
    # página.
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Se inicializa una cadena de texto vacía para almacenar el contenido HTML
    # que se va a generar.
    contenido_html = ''

    # Se agrega un encabezado de sección al contenido HTML. *
    contenido_html += '<div style = "background-color: #47a3cb; color: white;">'

    # Se busca el título de la página y se agrega al contenido HTML.
    title = soup.find('h1')
    contenido_html += str(title) + '\n'

    # OBTENCIÓN DE INFORMACIÓN DE LA URL

    # Si el tipo de astro es 'planet', se buscan los párrafos antes del div
    # con el primer encabezado de sección y se agregan al contenido HTML.
    if astro_type == 'planet':

        siblings = title.find_next_siblings()

        # Buscar los párrafos antes del div
        for sibling in siblings:
            if sibling.name == 'div':
                continue
            elif sibling.name == 'h2':
                break
            elif sibling.name == 'p':
                # Busca cada elemento nieto que sea un enlace
                grandchildren = sibling.find_all('a')

                # Reemplaza la URL de cada enlace que no provenga del sitio web
                # "universeguide.com" con la URL base
                for children in grandchildren:
                    if "universeguide.com" not in str(children['href']):
                        children['href'] = "https://universeguide.com" + \
                            str(children['href'])

                contenido_html += str(sibling) + '\n'

        # Se busca el primer elemento <h2> que contenga un elemento <id> con el
        # texto 'facts'
        facts_title = soup.find('h2', {'id': 'facts'})
        contenido_html += str(facts_title) + '\n'

        # Se busca el primer elemento hermano siguiente que sea una lista (ul)
        facts_list = facts_title.find_next_sibling('ul')

        # Se busca todos los elementos de lista (li) dentro de la lista y se
        # agregan al contenido HTML.
        facts_items = facts_list.find_all('li')

        contenido_html += '<ul>' + '\n'

        # Imprime el texto de cada elemento de la lista
        for item in facts_items:
            contenido_html += str(item) + '\n'

        contenido_html += '</ul>' + '\n'

        # Agregar la imagen del planeta
        # Se busca si existe una imagen en el HTML
        try:
            image = soup.find("img", {"class": "deskview"})

            # Se hace el tratamiento de la URL fuente de la imagen
            if "universeguide.com" not in str(image["src"]):
                image["src"] = "https://universeguide.com" + str(image["src"])

            # Se agrega la imagen a contenido_html alineada al centro
            contenido_html += '<div style="text-align:center">' + \
                str(image) + "</div>"

        # Si no existe la imagen, manejamos la excepción
        except BaseException:
            pass

        # Se agrega el el "closing tag"
        contenido_html += "</div>"

    # Si el tipo de astro corresponde a una estrella
    else:
        # Busca el contenedor principal de información de la estrella
        info = soup.find('div', {'id': 'divinfo'})

        # Busca cada elemento hijo del contenedor
        for item in info.children:
            if item.name == 'p':
                # Busca cada elemento nieto que sea un enlace
                grandchildren = item.find_all('a')
                # Reemplaza la URL de cada enlace que no provenga del sitio web
                # "universeguide.com" con la URL base
                for children in grandchildren:
                    if "universeguide.com" not in str(children['href']):
                        children['href'] = "https://universeguide.com" + \
                            str(children['href'])

                # Agrega el contenido HTML del párrafo al resultado final
                contenido_html += str(item) + '\n'

            # Detiene la búsqueda si el elemento hijo es un titulo
            elif item.name == 'h2':
                break

        # Busca el primer elemento hermano siguiente que sea una lista (ul)
        facts_list = info.find('ul')

        # Busca todos los elementos de lista (li) dentro de la lista
        facts_items = facts_list.find_all('li')

        contenido_html += '<ul>' + '\n'

        # Agrega cada elemento de la lista al resultado final
        for item in facts_items:
            contenido_html += str(item) + '\n'

        # Cierra la etiqueta HTML de la lista
        contenido_html += '</ul>' + '\n'

        # Se busca si existe una imagen en el HTML
        try:
            image = soup.find("img", {"class": "deskview"})

            # Se hace el tratamiento de la URL fuente de la imagen
            if "universeguide.com" not in str(image["src"]):
                image["src"] = "https://universeguide.com" + str(image["src"])

            # Se agrega la imagen a contenido_html alineada al centro
            contenido_html += '<div style="text-align:center">' + \
                str(image) + "</div>"

        # Si no existe la imagen, manejamos la excepción
        except BaseException:
            pass

        # Cierra el div que contiene la información de la estrella
        contenido_html += "</div>"

    # Retorna el contenido HTML obtenido para la información del planeta o
    # estrella.
    return contenido_html


def map_info(culture, stars_names=None, planet=None):
    """Función que devuelve información sobre constelaciones, estrellas y
    planetas.

    Args:
    - culture (str): nombre de la cultura para obtener la descripción de la
      constelación.
    - stars_names (list): lista de nombres de estrellas para obtener su
      información.
    - planet (str): nombre del planeta para obtener su información.

    Returns:
    - contenido_html (dict): diccionario con los contenidos HTML.

    """
    # Diccionario donde guardaremos la informacion obtenida para cada tipo de
    # objeto
    contenido_html = {}

    # Ruta del archivo de descripción de la cultura.
    culture_path = join(
        join(
            dirname(
                dirname(
                    dirname(
                        abspath(__file__)))),
            'StarMapGenerator'),
        'ConstellationsDescriptions')

    # Se abre el archivo y se lee su contenido.
    with open(join(culture_path, f'description_{culture}.utf8'), 'r',
              encoding='utf-8') as archivo:
        culture_content = archivo.read()

    # Se agrega la descripción de la constelación en el diccionario como
    # contenido HTML.
    contenido_html['Constellation'] = '<div style = "background-color: #47a3cb; color: white;">' + \
        str(culture_content) + "</div>"

    # Si se proporcionan nombres de estrellas, se busca la información
    # correspondiente y se agrega al diccionario.
    if stars_names:
        contenido_stars = []
        for star in stars_names:
            contenido_star = object_search('star', star)
            contenido_stars.append(contenido_star)
        contenido_html['Stars'] = contenido_stars

    # Si se proporciona el nombre de un planeta, se busca la información
    # correspondiente y se agrega al diccionario.
    if planet:
        contenido_planet = object_search('planet', planet)
        contenido_html['Planet'] = contenido_planet

    # Retorna el contenido HTML obtenido y contenido en el diccionario
    return contenido_html
