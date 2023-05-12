# hook-praw.py

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de datos necesarios para bs4
datas = collect_data_files('praw')