# hook-skyfield.py

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de datos necesarios para skyfield
datas = collect_data_files('skyfield')