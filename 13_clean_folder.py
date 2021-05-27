import os
import sys
import shutil


path_1 = 'input_data'
path_2 = 'output_data'
path_3 = 'teporary_file'
path_4 = '__pycache__'

folder_list = [path_1, path_2, path_3, path_4]

for folder_to_delete in folder_list:
    try:
        shutil.rmtree(folder_to_delete)
        print('eliminata')
    except OSError as e:
        print("Errore: %s - %s." % (e.filename, e.strerror))


