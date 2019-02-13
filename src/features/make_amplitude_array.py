# !/usr/bin/env python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from pydub import AudioSegment
from os import listdir
from settings import NUMBER_OF_CORES

# alternative dir
if len(sys.argv) > 1:
    from settings import REAL_DATA_CUT as CUT_DIR, REAL_DATA_AMP as AMPLITUDE_ARRAY_PATH
else:
    from settings import CUT_DIR, AMPLITUDE_ARRAY_PATH

import h5py
import numpy as np


def zero_noise(Sxx):
    # 50 db is like quiet restaurant
    # 10 * log10(x) = 50
    CUTOFF_THRESHOLD = 100000
    Sxx[Sxx < CUTOFF_THRESHOLD] = 0
    return Sxx


def create_folder_amplitude_array(folder):
    folder_files = listdir(os.path.join(CUT_DIR, folder))
    create_directory(os.path.join(AMPLITUDE_ARRAY_PATH))

    array_file = h5py.File(os.path.join(AMPLITUDE_ARRAY_PATH, folder + '.hdf5'), 'w')

    number_of_images = len(folder_files)
    all_norm_amplitudes = []
    for i, file in enumerate(folder_files):

        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))

        # read in a wav file
        data = AudioSegment.from_file(os.path.join(CUT_DIR, folder, file), format='wav')

        fft = np.fft.fft(np.array(data.get_array_of_samples()))
        N = fft.size
        f = abs(np.fft.fftfreq(N) * data.frame_rate)

        fft = zero_noise(fft)

        amplitudes = abs(fft) ** 2

        max_amplitude = amplitudes.max() if amplitudes.max() != 0 else 1
        norm_amplitudes = amplitudes / max_amplitude
        all_norm_amplitudes.append(norm_amplitudes)

    amplitudes = array_file.create_dataset(
        'amplitudes',
        data=all_norm_amplitudes,
        dtype='f'
    )

    # PY3 unicode
    dt = h5py.special_dtype(vlen=str)
    labels = array_file.create_dataset(
        'labels',
        data=np.transpose([folder.encode('utf8')] * len(all_norm_amplitudes)),
        dtype=dt
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
