# hook-tzwhere.py

from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['tzwhere', 'tzwhere.tzwhere']
# Incluir los archivos de datos necesarios para tzwhere
datas = collect_data_files('tzwhere') + collect_data_files('tzwhere.tzwhere')