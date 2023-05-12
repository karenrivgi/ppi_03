# hook-stdiomask.py

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de datos necesarios para stdiomask
datas = collect_data_files('stdiomask')