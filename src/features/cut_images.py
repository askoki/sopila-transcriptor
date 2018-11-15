import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import FILTER_SPECTROGRAM_DIR, CUT_DIR
from os import listdir
from PIL import Image


def crop_vertically(image, save_path, width, image_order):
    img_width, img_height = image.size

    # how many little image parts will be created
    steps = int(img_width / width)
    for i in range(steps):
        box = (i * width, 0, i * width + width, img_height)
        cropped_image = image.crop(box)
        cropped_image.save(save_path + str(image_order) + '.png', 'PNG')
        image_order += 1
    return image_order

image_folders = listdir(FILTER_SPECTROGRAM_DIR)
image_folders.sort()

for folder in image_folders:
    folder_files = listdir(FILTER_SPECTROGRAM_DIR + folder + '/')
    img_order = 1
    for file in folder_files:
        image = Image.open(FILTER_SPECTROGRAM_DIR + folder + '/' + file)
        img_order = crop_vertically(image, CUT_DIR + folder + '/', 20, img_order)
