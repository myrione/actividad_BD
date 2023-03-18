
El archivo proyecto se ha creado trabajando con un entorno virtual.

Para poder ejecutar el bot, es necesario instalar el paquete python-telegram-bot. 
La versión empleada de Python es 3.10 (consultar
el archivo pipfile.lock para ver las versiones y dependencias exactas).

Para poder probar las funciones del bot, es necesario disponer de una cuenta en Telegram.

_____ _________________ _______________

El bot se compone de los siguientes archivos:

-BPBot.py: es el punto de entrada al bot y contiene el main.
-commands.py: archivo que contiene la clase Commands con todos los comandos incluidos 
en el bot, a excepción del comando /start, que se encuentra en el archivo data_gathering.py.
-Config.py: archivo de configuración del bot
-data_gathering.py: archivo que contiene la clase DataGathering con todos los métodos 
utilizados para recabar la información de los nuevos usuarios y almacenarla en la 
base de datos. El punto de entrada para la recopilación de datos es el comando /start. La base
de datos se crea en la carpeta "assets" incluida en el directorio raíz del paquete.
-dbhelper.py: archivo que contiene la clase DBHelper que contiene todos los métodos 
necesarios para interactuar con la base de datos.
-metrics.py: archivo que contiene la clase Metrics, que recopila la información de mercado sobre Bitcoin mediante web scraping. 