import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import SPECTROGRAM_PATH, FILTER_SPECTROGRAM_DIR, FILTER_DIR
from PIL import Image
from os import listdir

# remove hidden files
images_folders = [f for f in listdir(SPECTROGRAM_PATH) if not f.startswith('.')]
images_folders.sort()

foreground = Image.open(FILTER_DIR + 'filter.png').convert('RGBA')

for folder in images_folders:
    folder_files = listdir(SPECTROGRAM_PATH + folder + '/')
    for image in folder_files:
        background = Image.open(SPECTROGRAM_PATH + folder + '/' + image).convert('RGBA')
        background.paste(foreground, (0, 0), foreground)
        background.save(FILTER_SPECTROGRAM_DIR + folder + '/' + image[:-4] + '+filter.png')
