# !/usr/bin/env python
import os
import sys
import h5py
import numpy as np
import array
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from helpers.data_helpers import natural_sort, get_folder_class_index
from pydub import AudioSegment
from pydub.utils import get_array_type
from os import listdir
from settings import NUMBER_OF_CORES

if not sys.argv[1]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[1])

if not sys.argv[2]:
    print('Enter path of cut data dir')
    sys.exit()

CUT_DIR = os.path.join(str(sys.argv[2]), ML_MODEL)

if not sys.argv[3]:
    print('Enter amplitude array path')
    sys.exit()

UNFILTERED_PATH = os.path.join(str(sys.argv[3]), ML_MODEL)

if not sys.argv[4]:
    print('Enter boolean is model random forest or CNN')
    sys.exit()

is_random_forest = (sys.argv[4] == 'True')


def create_folder_raw_array(folder):
    folder_files = listdir(os.path.join(CUT_DIR, folder))
    folder_files = natural_sort(folder_files)

    create_directory(os.path.join(UNFILTERED_PATH))

    array_file = h5py.File(os.path.join(
        UNFILTERED_PATH, folder + '.hdf5'), 'w')

    number_of_images = len(folder_files)
    all_data = []
    for i, file in enumerate(folder_files):

        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))

        # read in a wav file
        data = AudioSegment.from_file(
            os.path.join(CUT_DIR, folder, file), format='wav'
        )

        bit_depth = data.sample_width * 8
        array_type = get_array_type(bit_depth)

        numeric_array = array.array(array_type, data._data)
        all_data.append(numeric_array)

    amplitudes = array_file.create_dataset(
        'waveform',
        data=all_data,
        dtype='i'
    )

    folder_index = get_folder_class_index(CUT_DIR, folder)
    if is_random_forest:
        # PY3 unicode
        dt = h5py.special_dtype(vlen=str)
        array_file.create_dataset(
            'labels',
            data=np.transpose([folder.encode('utf8')] * len(all_data)),
            dtype=dt
        )
    else:
        array_file.create_dataset(
            'labels',
            data=np.transpose([folder_index] * len(all_data)),
            dtype='i'
        )


# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    # delete old unfiltered data (if exists)
    clear_dir(UNFILTERED_PATH)

    recordings_folders = listdir(os.path.join(CUT_DIR))
    recordings_folders.sort()
    # create_folder_raw_array(recordings_folders[0])
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(create_folder_raw_array, recordings_folders)
