import urllib.request
import tkinter as tk
from tkhtmlview import HTMLLabel

urls = {'https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/modern/description.en.utf8': 'modern',
        'https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/maya/description.en.utf8': 'maya',
        'https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/chinese/description.en.utf8': 'chinese',
        'https://raw.githubusercontent.com/Stellarium/stellarium/master/skycultures/egyptian/description.en.utf8': 'egyptian'}


for url, culture in urls.items():
    # agrega la cultura al nombre del archivo
    filename = f'description_{culture}.utf8'
    # descarga el archivo desde la URL y lo guarda con el nombre obtenido
    urllib.request.urlretrieve(url, filename)

# Abrir un archivo con formato utf-8 y leer su contenido
with open('description_modern.utf8', 'r', encoding='utf-8') as archivo:
    contenido = archivo.read()

with open('description_maya.utf8', 'r', encoding='utf-8') as archivo:
    contenido1 = archivo.read()

with open('description_chinese.utf8', 'r', encoding='utf-8') as archivo:
    contenido2 = archivo.read()

with open('description_egyptian.utf8', 'r', encoding='utf-8') as archivo:
    contenido3 = archivo.read()

ventana = tk.Tk()
ventana.title("Mi aplicación")

# Add label
my_label1 = HTMLLabel(ventana, html=contenido1)
my_label2 = HTMLLabel(ventana, html=contenido2)
my_label3 = HTMLLabel(ventana, html=contenido3)

# Adjust label
my_label1.pack(pady=10, padx=10)
my_label2.pack(pady=10, padx=10)
my_label3.pack(pady=10, padx=10)

ventana.mainloop()
