import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import TRAINING_DIR, TEST_DIR, FILTER_SPECTROGRAM_DIR, \
    VALIDATION_DIR, SPECTROGRAM_PATH
from helpers.file_helpers import create_directory, clear_dir
from os import listdir
from shutil import copy2
from random import shuffle
import sys

clear_dir(TRAINING_DIR)
clear_dir(VALIDATION_DIR)
clear_dir(TEST_DIR)

if len(sys.argv) > 1:
    # if no_filter is set to true than data is extracted from spectrogram folder
    no_filter = bool(sys.argv[1])
    FILTER_SPECTROGRAM_DIR = SPECTROGRAM_PATH if no_filter else FILTER_SPECTROGRAM_DIR


def copy_data_files(folder_files, folder, destination_folder=None, training_volume=0.8):
    validation_volume = 0.1

    copy_source_path = os.path.join(FILTER_SPECTROGRAM_DIR, folder)
    if not destination_folder:
        destination_folder = folder

    create_directory(os.path.join(TRAINING_DIR, destination_folder))
    create_directory(os.path.join(VALIDATION_DIR, destination_folder))
    create_directory(os.path.join(TEST_DIR, destination_folder))

    train_split_index = int(training_volume * len(folder_files))
    test_split_index = int(
        (training_volume + validation_volume) * len(folder_files)
    )

    training_files = folder_files[:train_split_index]
    for filename in training_files:
        copy2(
            os.path.join(copy_source_path, filename),
            os.path.join(TRAINING_DIR, destination_folder, filename)
        )

    validation_files = folder_files[train_split_index:test_split_index]
    for filename in validation_files:
        copy2(
            os.path.join(copy_source_path, filename),
            os.path.join(VALIDATION_DIR, destination_folder, filename)
        )

    test_files = folder_files[test_split_index:]
    for filename in test_files:
        copy2(
            os.path.join(copy_source_path, filename),
            os.path.join(TEST_DIR, destination_folder, filename)
        )


NUMBER_PER_TONE = 2000
# number of exampels per sopila tone
FOREIGN_SOPILA_NUM = int(NUMBER_PER_TONE / 6 / 4)

folders = listdir(FILTER_SPECTROGRAM_DIR)
folders.sort()

model_folder = listdir(os.path.join(FILTER_SPECTROGRAM_DIR))

for folder in model_folder:
    folder_files = listdir(os.path.join(FILTER_SPECTROGRAM_DIR, folder))

    # randomize data
    for i in range(100):
        shuffle(folder_files)

    if not 'silence' in folder:
        folder_files = folder_files[:NUMBER_PER_TONE]

    copy_data_files(
        folder_files,
        folder,
        training_volume=0.8
    )
