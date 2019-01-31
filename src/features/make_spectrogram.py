# !/usr/bin/env python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from scipy.signal import spectrogram
from pydub import AudioSegment
from os import listdir
from settings import NUMBER_OF_CORES

# alternative dir
if len(sys.argv) > 1:
    from settings import REAL_DATA_CUT as CUT_DIR, REAL_DATA_SPEC as SPECTROGRAM_PATH
else:
    from settings import CUT_DIR, SPECTROGRAM_PATH

from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import numpy as np


def convert_to_dB_and_normalize(Sxx):
    dBS = 10 * np.log10(Sxx)  # convert to dB
    # 30 do is like Quiet rural area
    # 10 db is like Breathing.
    CUTOFF_THRESHOLD_DB = 25
    # all values below threshold are set to 0 db
    dBS[dBS < CUTOFF_THRESHOLD_DB] = 0
    return dBS


def create_folder_spectrograms(folder):
    folder_files = listdir(os.path.join(CUT_DIR, folder))
    create_directory(os.path.join(SPECTROGRAM_PATH, folder))

    number_of_images = len(folder_files)
    for i, file in enumerate(folder_files):
        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))

        # read in a wav file
        data = AudioSegment.from_file(os.path.join(CUT_DIR, folder, file), format='wav')
        
        # Create Figure and Axes instances
        fig = plt.figure(frameon=False)
        # 20 x 480 pixels
        fig.set_size_inches(0.2, 4.8)

        # save fig with only spectogram content
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        
        f, t, Sxx = spectrogram(
            np.array(data.get_array_of_samples()), 
            data.frame_rate
        )
        dBS = convert_to_dB_and_normalize(Sxx)

        # if array of segment times is less then 1 (that happens in case of 10ms)
        # then hardcode values in order to plot spectrogram with pcolormesh
        # pcolormesh requires that t has at least 2 values
        if len(t) <= 1:
            t = np.array([0.00290249, 0.00798186])

        plt.pcolormesh(t, f, dBS, norm=Normalize(vmin=0))
        plt.ylim(0, 3000)

        # remove .wav
        image_name = file[:-4]

        plt.savefig(os.path.join(SPECTROGRAM_PATH, folder, image_name + '.jpg'))
        plt.close()


# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    # delete old spectrogram data (if exists)
    clear_dir(SPECTROGRAM_PATH)

    recordings_folders = listdir(os.path.join(CUT_DIR))
    recordings_folders.sort()
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(create_folder_spectrograms, recordings_folders)
