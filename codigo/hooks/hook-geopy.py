# hook-geopy.py

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('geopy')
# Incluir los archivos de datos necesarios para geopy
datas = collect_data_files('geopy')