from PyInstaller.utils.hooks import collect_data_files

hiddenimports = ['tzdata']

datas = collect_data_files('tzdata')
