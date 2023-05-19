# hook-tzwhere.py

from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['tzwhere']
# Incluir los archivos de datos necesarios para tzwhere
datas = collect_data_files('tzwhere')