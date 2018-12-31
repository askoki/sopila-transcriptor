import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import FILTER_DIR
from helpers.file_helpers import create_directory, clear_dir
from PIL import Image
from os import listdir

if len(sys.argv) > 1:
    from settings import REAL_DATA_SPEC as SPECTROGRAM_PATH, REAL_DATA_FILTER_SPEC as FILTER_SPECTROGRAM_DIR
else:
    from settings import SPECTROGRAM_PATH, FILTER_SPECTROGRAM_DIR
# delete old filter spectrogram data (if exists)
clear_dir(FILTER_SPECTROGRAM_DIR)

foreground = Image.open(FILTER_DIR + 'filter2.png').convert('RGBA')

models_folders = listdir(SPECTROGRAM_PATH)
models_folders.sort()

for model in models_folders:

    images_folders = listdir(SPECTROGRAM_PATH + model + '/')
    images_folders.sort()

    for folder in images_folders:
        folder_files = listdir(SPECTROGRAM_PATH + model + '/' + folder + '/')

        create_directory(FILTER_SPECTROGRAM_DIR + model + '/' + folder + '/')
        for image in folder_files:

            background = Image.open(
                SPECTROGRAM_PATH + model + '/' + folder + '/' + image
            ).convert('RGBA')

            background.paste(foreground, (0, 0), foreground)
            background.save(
                FILTER_SPECTROGRAM_DIR + model + '/' +
                folder + '/' + image[:-4] + '+filter.png'
            )
