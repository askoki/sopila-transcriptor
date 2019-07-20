# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', 'features'))


from google_drive_downloader import GoogleDriveDownloader as gdd
from helpers.file_helpers import clear_dir, create_directories, create_directory
from settings import REAL_DATA_DIR, REAL_DATA_CUT, REAL_DATA_RAW, \
    REAL_DATA_AMP, SHEETS_DIR, REAL_DATA_PREDICTIONS, ML_MODELS


# delete contents of raw directory
clear_dir(REAL_DATA_RAW)

directories_to_create = [
    REAL_DATA_DIR,
    REAL_DATA_RAW,
    os.path.join(REAL_DATA_RAW, 'mono'),
    os.path.join(REAL_DATA_RAW, 'poly')
]
create_directories(directories_to_create)

MONO_FILE_ID = '1nJyTa32Tk5gUOocqmQqdtPYsIOmDUqeT'
POLY_FILE_ID = '16BRz6UD-YDoRM7hlTUqI9WMH7IQYDAV6'

DATA_FILES = [
    (MONO_FILE_ID, os.path.join(REAL_DATA_RAW, 'mono')),
    (POLY_FILE_ID, os.path.join(REAL_DATA_RAW, 'poly'))
]
for FILE_ID, FILE_PATH in DATA_FILES:
    gdd.download_file_from_google_drive(
        file_id=FILE_ID,
        dest_path=os.path.join(FILE_PATH, 'data.zip'),
        unzip=True
    )
    print("Removing downloaded zip file ...")
    os.remove(os.path.join(FILE_PATH, 'data.zip'))

# create base data folder structure
directories_to_create = [
    REAL_DATA_CUT,
    REAL_DATA_AMP,
    REAL_DATA_PREDICTIONS,
    SHEETS_DIR
]

# create directories in data folder
create_directories(directories_to_create)
for directory in directories_to_create:
    for model in ML_MODELS:
        create_directory(os.path.join(directory, model['name']))
