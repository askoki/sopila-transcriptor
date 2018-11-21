# -*- coding: utf-8 -*-
from os import remove, path
import sys
sys.path.insert(1, path.join(sys.path[0], '../..'))

from settings import RAW_DATA_DIR
from google_drive_downloader import GoogleDriveDownloader as gdd

FILE_ID = '1jMiQ4iMKaUgN3EDFPS5sSFfRDCH-5Bne'
gdd.download_file_from_google_drive(
    file_id=FILE_ID,
    dest_path=RAW_DATA_DIR + 'data.zip',
    unzip=True
)

print("Removing downloaded zip file ...")
remove(RAW_DATA_DIR + 'data.zip')
