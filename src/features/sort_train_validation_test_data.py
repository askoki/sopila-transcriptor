import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import TRAINING_DIR, TEST_DIR, FILTER_SPECTROGRAM_DIR, \
    VALIDATION_DIR
from helpers.file_helpers import create_directory, clear_dir
from os import listdir, remove
from shutil import copy2
from random import shuffle

clear_dir(TRAINING_DIR)
clear_dir(VALIDATION_DIR)
clear_dir(TEST_DIR)


def copy_data_files(folder_files, model, folder, destination_folder=None, training_volume=0.8):
    validation_volume = 0.1

    copy_source_path = FILTER_SPECTROGRAM_DIR + model + '/' + folder + '/'
    if not destination_folder:
        destination_folder = folder

    create_directory(TRAINING_DIR + model + '/' + destination_folder + '/')
    create_directory(VALIDATION_DIR + model + '/' + destination_folder + '/')
    create_directory(TEST_DIR + model + '/' + destination_folder + '/')

    train_split_index = int(training_volume * len(folder_files))
    test_split_index = int(
        (training_volume + validation_volume) * len(folder_files)
    )

    training_files = folder_files[:train_split_index]
    for filename in training_files:
        copy2(
            copy_source_path + filename,
            TRAINING_DIR + model + '/' + destination_folder + '/' + filename
        )

    validation_files = folder_files[train_split_index:test_split_index]
    for filename in validation_files:
        copy2(
            copy_source_path + filename,
            VALIDATION_DIR + model + '/' + destination_folder + '/' + filename
        )

    test_files = folder_files[test_split_index:]
    for filename in test_files:
        copy2(
            copy_source_path + filename,
            TEST_DIR + model + '/' + destination_folder + '/' + filename
        )


NUMBER_PER_TONE = 2000
# number of exampels per sopila tone
FOREIGN_SOPILA_NUM = int(NUMBER_PER_TONE / 6 / 4)

folders = listdir(FILTER_SPECTROGRAM_DIR)
folders.sort()


models_folders = listdir(FILTER_SPECTROGRAM_DIR)
models_folders.sort()

all_files_per_model = {}

for model in models_folders:

    model_folder = listdir(FILTER_SPECTROGRAM_DIR + model + '/')
    model_folder.sort()

    all_files_per_model[model] = {}

    for folder in model_folder:

        folder_files = listdir(FILTER_SPECTROGRAM_DIR +
                               model + '/' + folder + '/')

        # randomize data
        for i in range(100):
            shuffle(folder_files)

        if not 'silence' in folder:
            folder_files = folder_files[:NUMBER_PER_TONE]
            # sopila tones to insert as class in opposite model (ex. m in v)
            all_files_per_model[model][folder] = folder_files[:FOREIGN_SOPILA_NUM]

        copy_data_files(
            folder_files,
            model,
            folder,
            training_volume=0.8
        )

# add opposite model in model data
# m in v and opposite

# for folder, files in all_files_per_model['v'].items():
#     copy_data_files(
#         files,
#         'v',
#         folder,
#         'other'
#     )

# for folder, files in all_files_per_model['m'].items():
#     copy_data_files(
#         files,
#         'm',
#         folder,
#         'other'
#     )
