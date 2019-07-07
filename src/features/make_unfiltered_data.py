# !/usr/bin/env python
import os
import sys
import h5py
import numpy as np
import array
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from helpers.data_helpers import natural_sort
from pydub import AudioSegment
from pydub.utils import get_array_type
from os import listdir
from settings import NUMBER_OF_CORES, CUT_DIR, UNFILTERED_PATH


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

    # PY3 unicode
    dt = h5py.special_dtype(vlen=str)
    labels = array_file.create_dataset(
        'labels',
        data=np.transpose([folder.encode('utf8')] * len(all_data)),
        dtype=dt
    )


# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    # delete old amplitude array data (if exists)
    clear_dir(UNFILTERED_PATH)

    recordings_folders = listdir(os.path.join(CUT_DIR))
    recordings_folders.sort()
    # create_folder_raw_array(recordings_folders[0])
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(create_folder_raw_array, recordings_folders)
