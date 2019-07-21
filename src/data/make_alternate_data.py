# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', 'features'))


from google_drive_downloader import GoogleDriveDownloader as gdd
from helpers.file_helpers import clear_dir, create_directories, create_directory
from settings import REAL_DATA_DIR, REAL_DATA_CUT, REAL_DATA_RAW, \
    REAL_DATA_AMP, SHEETS_DIR, REAL_DATA_PREDICTIONS, \
    ML_MODELS, REAL_DATA_UNFILTERED


# delete contents of raw directory
clear_dir(REAL_DATA_RAW)

# create directories in data folder
create_directory(REAL_DATA_DIR)

directories_to_create = [
    REAL_DATA_RAW,
    REAL_DATA_PREDICTIONS,
    REAL_DATA_CUT,
    SHEETS_DIR,
    REAL_DATA_AMP,
    REAL_DATA_UNFILTERED
]
for directory in directories_to_create:
    for model in ML_MODELS:
        if directory == REAL_DATA_AMP and model['unfiltered']:
            continue

        if directory == REAL_DATA_UNFILTERED and not model['unfiltered']:
            continue
        create_directory(os.path.join(directory, model['name']))

MONO_FILE_ID = '1nJyTa32Tk5gUOocqmQqdtPYsIOmDUqeT'
POLY_FILE_ID = '16BRz6UD-YDoRM7hlTUqI9WMH7IQYDAV6'

for i, model in enumerate(ML_MODELS):
    model_dir = os.path.join(REAL_DATA_RAW, model['name'])

    if model['voice_type'] == 'mono':
        FILE_ID = '1nJyTa32Tk5gUOocqmQqdtPYsIOmDUqeT'
    else:
        FILE_ID = '16BRz6UD-YDoRM7hlTUqI9WMH7IQYDAV6'

    gdd.download_file_from_google_drive(
        file_id=FILE_ID,
        dest_path=os.path.join(REAL_DATA_RAW, model['name'], 'data.zip'),
        unzip=True
    )
    print("Removing downloaded zip file ...")
    os.remove(os.path.join(REAL_DATA_RAW, model['name'], 'data.zip'))
