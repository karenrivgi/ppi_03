# hook-tkhtmlview.py

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de datos necesarios para tkhtmlview
datas = collect_data_files('tkhtmlview')