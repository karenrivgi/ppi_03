# Py Man 's Sky
##### _El cielo en tu bolsillo_

Py Man's Sky tiene como objetivo acercar a las personas a la astronomía a través de un aplicativo que les permita generar un mapa personalizado del cielo, además de contener información relevante sobre estos temas.

### ¿Por qué el proyecto es útil?: 
La utilidad de este proyecto se enfoca en ser un contenido tanto didáctico como científico; didáctico porque puedes generar un mapa del cielo personalizado y científico ya que fomenta conocer más sobre la astronomía gracias al contenido sobre astros que presenta la aplicación, dentro del mapa, en su descripción y en la sección cultural dentro de esta. Esta sección cultural se enfoca en conocimiento sobre eventos científicos y culturales sobre la astronomía.

### Funcionalidades:
- Crear un mapa del cielo con datos personalizados ingresados por el usuario.
- Acceder a información sobre los astros observados dentro del mapa.
- Acceder a una sección cultural con publicaciones sobre astronomía.

### Tecnologías utilizadas:
- Lenguaje de programación Python y librerías de este como: Skyfield, Matplotlib, Geopy, Datetime, Numpy, Pandas, entre otros.
- Haremos uso de la página web Figma para el diseño de las interfaces y Tkinter para codificarlas.

### Guia de Instalación

Instalar las librerías requeridas:
```sh
pip install -r requirements.txt
```

| Librería | Versión |
| ------ | ------ |
| datetime | 5.1|
| geopy | 2.3.0 |
| tzwhere | 3.0.3 |
| pytz | 2022.7 |
| numpy | 1.23.5 |
| pandas | 1.5.2 |
| skyfield | 1.45 |
| matplotlib | 3.6.2 |
| stdiomask | 0.0.6 |
| praw | 7.7.0 |


### Autores:
- [@YamidCampo](https://github.com/YamidCampo): Yamid Andrés Campo Gallego.
- [@JEROLPOA2](https://github.com/JEROLPOA2): Jerónimo Ledesma Patiño.
- [@DavedCV](https://github.com/DavedCV): David Castrillón Vallejo.
- [@karenrivgi](https://github.com/karenrivgi): Karen Rivera Giraldo.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

### Descripción de la funcionalidad del proyecto:
- La aplicación de escritorio presentará una interfaz amigable para la exploración sencilla de la astronomía por medio de la inmersión a mapas estelares. 
- Los usuarios del aplicativo tendrán la opción de registrarse con un nombre de usuario y contraseña que les permitirá acceder a funcionalidades adicionales y guardar ciertos datos.
- **Funcionalidades para usuarios registrados.**
-- Generación de un mapa estelar personalizado; dicha personalización se basa en la selección de constelación visibles por cultura, fecha específica de la visualización, lugar geográfico de observación, variación de cantidad de estrellas visibles, y la posibilidad de habilitar y deshabilitar los nombres de las estrellas más importantes.
-- Permitirle al usuario visualizar un planeta del sistema solar (si es que está visible para la ubicación y fecha proporcionadas) sobre el mapa estelar.
Consultar información relevante acerca de las estrellas más importantes mostradas en el mapa generado, proveniente de páginas web que contienen datos sobre dichos astros.
-- Tener acceso a la sección cultural y de entretenimiento, donde el usuario podrá visualizar las tendencias en subreddits relacionadas con astronomía y ciencia.
-- Mostrar información sobre la cultura que dió origen a las constelaciones que se muestran en el mapa.
-- Tener la posibilidad de publicar su mapa del cielo en Reddit, en el subreddit exclusivo de la aplicación.
-- Permitir al usuario descargar el mapa generado como una imagen.
-- Permitir al usuario guardar en un historial los datos de entrada sobre los mapas que ha generado.
-- Guardar el historial de las últimas estrellas consultadas en los mapas estelares generados por el mismo.
-- Guardar el historial de publicaciones hechas en el subreddit compartiendo mapas de estrellas personalizados.
-- Consultar cuál es la fase de la luna correspondiente a una fecha ingresada y mostrarla con una imagen representativa.
-- Consultar cuándo será visible en el horizonte un objeto celeste seleccionado, en base a fecha(y ubicación).
- **Funcionalidades para usuarios no registrados:**
-- Generar un mapa estelar con las opciones predeterminadas por la aplicación en base a la ubicación ingresada por el usuario.
-- Mostrar información sobre la cultura que dió origen a las constelaciones que se muestran en el mapa.
--Permitir la visualización de los planetas que estén en el mapa generado.

 En base a las funcionalidades previstas para la aplicación, definimos las siguientes actividades a desarrollar para construirlas:

- **Informe 03: 13 horas del viernes 24 de marzo, “Hola Mundo” de la aplicación:**
-- Interfaz simple para la interacción del usuario con el aplicativo.
-- Generación de un  mapa básico de estrellas a partir de los datos de ubicación y hora ingresados por el usuario (Conteniendo nombre de las estrellas más brillantes y muestra de las constelaciones modernas sobre el mapa)
-- Prueba de la conexión con la API de reddit y funcionalidad de publicar el mapa estelar en un subreddit propio de la aplicación.


- **Informe 04: 13 horas del viernes 31 de marzo.**
-- Implementación de la lógica orientada a objetos para la creación de usuarios.
-- Discretización de la interfaz para usuarios registrados y no registrados.
-- Refinamiento de la interfaz gráfica usando programación orientada a objetos.
    <br /><br />
    ![image](./aux_images/DiagramaDeClasesInterfaz.jpeg)
    <br />
-- Implementación de la descarga del mapa generado como imagen para usuarios registrados.
-- Aplicar la persistencia de datos para los usuarios creados, y un historial para los datos que ha ingresado al generar un mapa estelar.


- **Informe 05: 13 horas del viernes 14 de abril.** 
-- Implementación de opción que permita visualizar planetas del sistema solar en el mapa generado (si son visibles en la ubicación y hora proporcionadas).
-- Habilitación de las opciones para la modificación del mapa con los parámetros definidos, a los usuarios registrados.
-- Integración de funcionalidades API Reddit.
   + Publicación de los mapas generados por el usuario en el subreddit.
   + Guardar el historial de las publicaciones hechas en el subreddit.


- **Informe 06: 13 horas del viernes 21 de abril.**
  -- Implementación del sistema de búsqueda de objetos celestes y de la identificación de objetos en el mapa este ar generado:
  +  Extraer la información relevante sobre las estrellas más importantes de la página www.universeguide.com , que dado un número del catálogo de Hipparcos y el nombre de una estrella permite visualizar datos variados sobre este objeto.
  +  Exponer la información recolectada a un lado del mapa generado, listando únicamente las estrellas visibles en dicho mapa.
  + Implementación de historial para últimas estrellas consultadas.
  + Mostrar información sobre el contexto cultural de la constelación escogida para visualizarse en el mapa.


- **Informe 07: 13 horas del viernes 28 de abril.**
  -- Implementación de sección cultural y de entretenimiento en la interfaz.
  + Se proporcionarán publicaciones, información y eventos astronómicos extraídos por medio de web scraping y de las APIS.
  + Modificar la interfaz de modo que estas publicaciones puedan ser observadas en otra sección del aplicativo.


- **Informe 08: 13 horas del viernes 5 de mayo.**
-- Creación de la sección para consultar cuál es la fase de la luna correspondiente a una fecha ingresada.
-- Manejo de excepciones para las entradas de los usuarios.
-- Optimización y refinamiento de funcionalidades e interfaces.


- **Informe 09: 13 horas del viernes 12 de mayo.**
  -- Conclusión optimización de la interfaz de la aplicación.
  -- Creación de la funcionalidad para consultar cuándo será visible en el horizonte un objeto celeste seleccionado, en base a fecha (y ubicación).


- **Informe 10: 13 horas del viernes 26 de mayo.**
-- Correcciones y ajustes finales en base a la sustentación realizada del informe 09.
