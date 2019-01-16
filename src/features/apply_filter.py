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

def apply_filter_to_folder(folder):
    folder_files = listdir(os.path.join(SPECTROGRAM_PATH, folder))

    create_directory(os.path.join(FILTER_SPECTROGRAM_DIR, folder))
    for image in folder_files:

        background = Image.open(
            os.path.join(SPECTROGRAM_PATH, folder, image)
        ).convert('RGBA')

        background.paste(foreground, (0, 0), foreground)
        background.save(
            os.path.join(
                FILTER_SPECTROGRAM_DIR, folder, image[:-4] + '+filter.png'
            )
        )


# delete old filter spectrogram data (if exists)
clear_dir(FILTER_SPECTROGRAM_DIR)

foreground = Image.open(os.path.join(FILTER_DIR, 'filter2.png')).convert('RGBA')

images_folders = listdir(os.path.join(SPECTROGRAM_PATH))
images_folders.sort()

# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(apply_filter_to_folder, images_folders)

