import datetime
import tkinter as tk
from tkinter import messagebox
from skymap import generar_mapa
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Variables para guardar la fecha y hora ingresadas por el usuario y la información de ubicación
fecha_hora_str = None
ubicacion_str = None

def mostrar_grafico():
    global fecha_hora_str, ubicacion_str
    
    # Crear la figura y el canvas
    fig = generar_mapa(fecha_hora_str, ubicacion_str)
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    
    # Agregar el canvas a la ventana de Tkinter
    canvas.get_tk_widget().grid(row=0, column=1, sticky='nsew')
    canvas.get_tk_widget().configure(width=600, height=600)

    # Mostrar la ventana de Tkinter
    ventana.mainloop()

# Función que se ejecuta al hacer clic en el botón "Guardar"
def guardar_datos():
    # Accedemos a las variables globales de fecha, hora y ubicación
    global fecha_hora_str, ubicacion_str

    # Obtenemos la fecha y hora ingresadas por el usuario
    fecha = entry_fecha.get()
    hora = entry_hora.get()

    # Convertimos la fecha y hora a objetos datetime
    fecha_obj = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    hora_obj = datetime.datetime.strptime(hora, '%H:%M')

    # Combinamos la fecha y hora en un solo objeto datetime
    fecha_hora_obj = fecha_obj.replace(hour=hora_obj.hour, minute=hora_obj.minute)

    # Convertimos el objeto datetime a una cadena de texto y lo guardamos en la variable global
    fecha_hora_str = fecha_hora_obj.strftime('%Y-%m-%d %H:%M')

    # Obtenemos los valores de los campos de entrada para la ubicación
    pais = entry_pais.get()
    departamento = entry_departamento.get()
    ciudad = entry_ciudad.get()

    # Unimos los valores en una cadena de texto separada por comas y lo guardamos en la variable global
    ubicacion_str = f"{pais}, {departamento}, {ciudad}"

    # Mostramos un mensaje al usuario indicando que los datos han sido guardados
    messagebox.showinfo("Guardado", "Los datos han sido guardados.")

    # Habilitar el botón "Mostrar gráfico"
    boton_mostrar.config(state='normal')
    

# Creamos la ventana principal
ventana = tk.Tk()
ventana.title("Ingreso de datos")
ventana.geometry('800x600')

sidebar = tk.Frame(ventana, width=200, height=600)
sidebar.grid(row=0, column=0, sticky='nsew')

# Creamos los widgets para ingresar la fecha y hora
label_fecha = tk.Label(sidebar, text="Fecha (AAA-MM-DD):")
label_fecha.grid(row=0, column=0)
entry_fecha = tk.Entry(sidebar)
entry_fecha.grid(row=1, column=0)

label_hora = tk.Label(sidebar, text="Hora (HH:MM):")
label_hora.grid(row=2, column=0)
entry_hora = tk.Entry(sidebar)
entry_hora.grid(row=3, column=0)

# Creamos los widgets para ingresar la ubicación
label_pais = tk.Label(sidebar, text="País:")
label_pais.grid(row=4, column=0)
entry_pais = tk.Entry(sidebar)
entry_pais.grid(row=5, column=0)

label_departamento = tk.Label(sidebar, text="Departamento:")
label_departamento.grid(row=6, column=0)
entry_departamento = tk.Entry(sidebar)
entry_departamento.grid(row=7, column=0)

label_ciudad = tk.Label(sidebar, text="Ciudad:")
label_ciudad.grid(row=8, column=0)
entry_ciudad = tk.Entry(sidebar)
entry_ciudad.grid(row=9, column=0)

# Creamos el botón para guardar los datos
boton_guardar = tk.Button(sidebar, text="Guardar", command=guardar_datos)
boton_guardar.grid(row=10, column=0)    

boton_mostrar = tk.Button(sidebar, text="Mostrar gráfico", command=mostrar_grafico, state='disabled')
boton_mostrar.grid(row=11, column=0)

# Iniciamos el bucle principal de la ventana
ventana.mainloop()

# Imprimimos el valor de las variables que contienen la fecha, hora y ubicación ingresadas por el usuario
print(fecha_hora_str)
print(ubicacion_str)
