import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import html2text
import tkinter as tk
from tkhtmlview import HTMLLabel

def object_search(astro_type, astro):

    if astro_type == 'planet':
        url = f"https://www.universeguide.com/{astro_type}/{astro}"
    else:
        names_path =  os.path.join(os.path.join(os.path.dirname(__file__),"StarMapGenerator"), "names.csv")
        names = pd.read_csv(names_path)

        # common name debe estar en mayúsculas
        url = names.loc[names['common name'] == astro, 'source'].values[0]

    # Obtener el contenido de la URL y analizar el contenido HTML de la misma
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    contenido_html = ''
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


    else:
        info = soup.find('div', {'id': 'divinfo'})

        for item in info.children:
            if item.name == 'p': 
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

    
    return contenido_html

# Pruebas para estrellas
astro_type = 'star'
astro = 'Polaris'

# Pruebas para planetas
#astro_type = 'planet'
#astro = 'earth'

contenido_html = object_search(astro_type, astro)

ventana = tk.Tk()
ventana.title("Mi aplicación")

# Add label
my_label = HTMLLabel(ventana, html=contenido_html)

# Adjust label
my_label.pack(pady=20, padx=20)

ventana.mainloop()