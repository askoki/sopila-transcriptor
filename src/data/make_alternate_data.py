# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', 'features'))


from google_drive_downloader import GoogleDriveDownloader as gdd
from helpers.file_helpers import clear_dir, create_directories
from settings import REAL_DATA_CUT, REAL_DATA_RAW, REAL_DATA_SPEC, \
    REAL_DATA_FILTER_SPEC, REAL_DATA_DIR


# create base data folder structure
directories_to_create = [
    REAL_DATA_DIR,
    REAL_DATA_CUT,
    REAL_DATA_RAW,
    REAL_DATA_SPEC,
    REAL_DATA_FILTER_SPEC
]

# create directories in data folder
create_directories(directories_to_create)

# delete contents of raw folder
clear_dir(REAL_DATA_RAW)


FILE_ID = '1F7NLHL862BSZ99s-HksYBX85XEu4sllI'
gdd.download_file_from_google_drive(
    file_id=FILE_ID,
    dest_path=os.path.join(REAL_DATA_RAW, 'data.zip'),
    unzip=True
)

print("Removing downloaded zip file ...")
os.remove(os.path.join(REAL_DATA_RAW, 'data.zip'))
