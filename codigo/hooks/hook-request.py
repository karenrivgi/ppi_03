# hook-request.py

from PyInstaller.utils.hooks import collect_data_files

# Incluir los archivos de datos necesarios para request
datas = collect_data_files('request')