import requests
from bs4 import BeautifulSoup
import os
from os.path import abspath, dirname, join
import pandas as pd
import html2text
import tkinter as tk
from tkhtmlview import HTMLLabel

def object_search(astro_type, astro):

    if astro_type == 'planet':
        url = f"https://www.universeguide.com/{astro_type}/{astro}"
    else:
        names_path =  join(join(dirname(dirname(dirname(abspath(__file__)))), 'StarMapGenerator'), "names.csv")
        names = pd.read_csv(names_path)

        # common name debe estar en mayúsculas
        #print(names.loc[names['common name'] == astro, 'source'])
        HIP = names.loc[names['common name'] == astro, 'HIP'].values[0]
        url = f"https://www.universeguide.com/{astro_type}/{HIP}/{astro}"


    # Obtener el contenido de la URL y analizar el contenido HTML de la misma
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    contenido_html = ''

    contenido_html += '<div style = "background-color: #47a3cb; color: white;">'
    
    title = soup.find('h1')
    contenido_html += str(title) +  '\n' 


    if astro_type == 'planet':
        
        siblings = title.find_next_siblings()

        # Buscar los párrafos antes del div
        for sibling in siblings:
            if sibling.name == 'div':
                continue
            elif sibling.name == 'h2':
                break
            elif sibling.name == 'p':
                grandchildren = sibling.find_all('a')
                for children in grandchildren:
                    if not "universeguide.com" in str(children['href']):
                        children['href'] = "https://universeguide.com" + str(children['href'])
                contenido_html += str(sibling) +  '\n' 

        # Busca el primer elemento <h2> que contenga un elemento <id> con el texto 'facts'
        facts_title = soup.find('h2', {'id': 'facts'})
        contenido_html += str(facts_title) +  '\n'

        # Busca el primer elemento hermano siguiente que sea una lista (ul)
        facts_list = facts_title.find_next_sibling('ul')

        # Busca todos los elementos de lista (li) dentro de la lista
        facts_items = facts_list.find_all('li') 

        contenido_html += '<ul>' +  '\n'

        # Imprime el texto de cada elemento de la lista
        for item in facts_items:
            contenido_html += str(item) +  '\n'

        
        contenido_html += '</ul>' +  '\n'

        # Agregar la imagen del planeta

        try:
            image = soup.find("img", {"class": "deskview"})

            if not "universeguide.com" in str(image["src"]):
                image["src"] = "https://universeguide.com" + str(image["src"])

            contenido_html += '<div style="text-align:center">' + str(image) + "</div>"
        except:
            print("no hay imagen")

        contenido_html += "</div>"

    else:
        info = soup.find('div', {'id': 'divinfo'})

        for item in info.children:
            if item.name == 'p': 
                grandchildren = item.find_all('a')
                for children in grandchildren:
                    if not "universeguide.com" in str(children['href']):
                        children['href'] = "https://universeguide.com" + str(children['href'])
                contenido_html += str(item) +  '\n'
            elif item.name == 'h2':
                break

        # Busca el primer elemento hermano siguiente que sea una lista (ul)
        facts_list = info.find('ul')

        # Busca todos los elementos de lista (li) dentro de la lista
        facts_items = facts_list.find_all('li') 

        contenido_html += '<ul>' +  '\n'

        # Imprime el texto de cada elemento de la lista
        for item in facts_items:
            contenido_html += str(item) +  '\n'
        
        contenido_html += '</ul>' +  '\n'

        try:
            image = soup.find("img", {"class": "deskview"})

            if not "universeguide.com" in str(image["src"]):
                image["src"] = "https://universeguide.com" + str(image["src"])

            contenido_html += '<div style="text-align:center">' + str(image) + "</div>"
        
        except:
            print("no hay imagen")

        contenido_html += "</div>"
    
    return contenido_html


def map_info(culture, stars_names = None, planet = None): 
    contenido_html = {}
    culture_path = join(join(dirname(dirname(dirname(abspath(__file__)))), 'StarMapGenerator'), 'ConstellationsDescriptions')
    
    with open(join(culture_path, f'description_{culture}.utf8') , 'r', encoding='utf-8') as archivo:
        culture_content = archivo.read()

    contenido_html['Constellation'] = culture_content

    if stars_names:
        contenido_stars = []
        for star in stars_names:
            contenido_star = object_search('star', star)
            contenido_stars.append(contenido_star)
        contenido_html['Stars'] = contenido_stars

    if planet:
        contenido_planet = object_search('planet', planet)
        contenido_html['Planet'] = contenido_planet

    return contenido_html

if __name__ == "__main__":
    # MUESTRA DE VISUALIZACIÓN EN TKINTER

    # Pruebas para estrellas
    astro_type = 'star'
    astro = 'Merak'

    # Pruebas para planetas
    #astro_type = 'planet'
    #astro = 'saturn'

    #contenido_html = object_search(astro_type, astro)

    stars_names = ['Acrux']
    planet = 'mars'

    contenido_html = map_info('chinese', stars_names, planet)
    ventana = tk.Tk()
    ventana.title("Mi aplicación")

    # Add label
    for key in contenido_html.keys():

        if key == 'Stars':

            for star in contenido_html[key]:
                my_label = HTMLLabel(ventana, html=star)

                # Adjust label
                my_label.pack(pady=5, padx=5, fill="both", expand=True)

        else:
            my_label = HTMLLabel(ventana, html=contenido_html[key])

            # Adjust label
            my_label.pack(pady=5, padx=5, fill="both", expand=True)

    ventana.mainloop()

