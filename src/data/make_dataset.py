# -*- coding: utf-8 -*-
import os
import sys
import subprocess
from google_drive_downloader import GoogleDriveDownloader as gdd
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from features.helpers.file_helpers import clear_dir, create_directories, create_directory
from settings import RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, \
    AMPLITUDE_ARRAY_PATH, CUT_DIR, STATISTICS_DIR, ML_MODELS, \
    FIGURES_DIR, UNFILTERED_PATH, MODEL_DIR

# delete contents of raw folder
clear_dir(RAW_DATA_DIR)

directories_to_create = [
    RAW_DATA_DIR,
    INTERIM_DATA_DIR
]
create_directories(directories_to_create)

# create base data folder structure
directories_to_create = [
    PROCESSED_DATA_DIR,
    AMPLITUDE_ARRAY_PATH,
    CUT_DIR,
    FIGURES_DIR,
    UNFILTERED_PATH,
    STATISTICS_DIR,
    MODEL_DIR
]

# create directories in data folder
create_directories(directories_to_create)
for directory in directories_to_create:
    for model in ML_MODELS:
        if directory == AMPLITUDE_ARRAY_PATH and model['unfiltered']:
            continue

        if directory == UNFILTERED_PATH and not model['unfiltered']:
            continue
        create_directory(os.path.join(directory, model['name']))


for i, model in enumerate(ML_MODELS):
    print("Downloading %d/%d" % (i + 1, len(ML_MODELS)))
    FILE_ID = '1SACjFsfdUZKVmBwV0bOMt9ni6B6DR6Dt'
    model_dir = os.path.join(RAW_DATA_DIR, model['name'])
    gdd.download_file_from_google_drive(
        file_id=FILE_ID,
        dest_path=os.path.join(model_dir, 'data.zip'),
        unzip=True
    )

    print("Removing downloaded zip file ...")
    os.remove(os.path.join(model_dir, 'data.zip'))
    if model['voice_type'] == 'poly':
        subprocess.call(
            ['python', 'merge_audio_data.py', model_dir],
            cwd="../features/"
        )
