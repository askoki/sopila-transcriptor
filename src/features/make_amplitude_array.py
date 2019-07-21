# !/usr/bin/env python
import faulthandler; faulthandler.enable()
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

import h5py
import numpy as np
from helpers.file_helpers import create_directory, clear_dir
from helpers.data_helpers import get_folder_class_index, natural_sort
from pydub import AudioSegment
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

AMPLITUDE_ARRAY_PATH = os.path.join(str(sys.argv[3]), ML_MODEL)

if not sys.argv[4]:
    print('Enter boolean is model random forest or CNN')
    sys.exit()

is_random_forest = (sys.argv[4] == 'True')


def normalize_amplitudes(amplitudes):
    # 50 db is like quiet restaurant
    # 10 * log10(x) = 50
    CUTOFF_THRESHOLD = 100000

    if amplitudes[amplitudes >= CUTOFF_THRESHOLD].any():
        amplitudes = abs(amplitudes) ** 2
        max_amplitude = amplitudes.max() if amplitudes.max() != 0 else 1.0
    else:
        # max threshold approx 20% of max value
        max_percentage = 0.2
        amplitudes = abs(amplitudes) * max_percentage
        max_amplitude = CUTOFF_THRESHOLD

    return amplitudes / max_amplitude


def create_folder_amplitude_array(folder):
    folder_files = listdir(os.path.join(CUT_DIR, folder))
    folder_files = natural_sort(folder_files)

    create_directory(os.path.join(AMPLITUDE_ARRAY_PATH))

    array_file = h5py.File(os.path.join(
        AMPLITUDE_ARRAY_PATH, folder + '.hdf5'),
        'w'
    )

    number_of_images = len(folder_files)
    all_norm_amplitudes = []
    for i, file in enumerate(folder_files):

        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))

        # read in a wav file
        data = AudioSegment.from_file(
            os.path.join(CUT_DIR, folder, file),
            format='wav'
        )

        fft = np.fft.fft(np.array(data.get_array_of_samples()))

        norm_amplitudes = normalize_amplitudes(fft)

        all_norm_amplitudes.append(norm_amplitudes)

    array_file.create_dataset(
        'amplitudes',
        data=all_norm_amplitudes,
        dtype='f'
    )

    folder_index = get_folder_class_index(CUT_DIR, folder)
    if is_random_forest:
        # PY3 unicode
        dt = h5py.special_dtype(vlen=str)
        array_file.create_dataset(
            'labels',
            data=np.transpose([folder.encode('utf8')] * len(all_norm_amplitudes)),
            dtype=dt
        )
    else:
        array_file.create_dataset(
            'labels',
            data=np.transpose([folder_index] * len(all_norm_amplitudes)),
            dtype='i'
        )


# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    # delete old spectrogram data (if exists)
    clear_dir(AMPLITUDE_ARRAY_PATH)

    recordings_folders = listdir(os.path.join(CUT_DIR))
    recordings_folders.sort()
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(create_folder_amplitude_array, recordings_folders)
