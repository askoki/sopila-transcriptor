#!/usr/bin/env python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from helpers.file_helpers import create_directory, clear_dir
from scipy.signal import stft, spectrogram
from scipy.io import wavfile
from os import listdir

# alternative dir
if len(sys.argv) > 1:
    from settings import REAL_DATA_CUT as CUT_DIR, REAL_DATA_SPEC as SPECTROGRAM_PATH
else:
    from settings import CUT_DIR, SPECTROGRAM_PATH

import matplotlib.pyplot as plt
import numpy as np
import wave
import pylab

# delete old spectrogram data (if exists)
clear_dir(SPECTROGRAM_PATH)

# remove hidden files
# recordings_folders = [f for f in listdir(CUT_DIR) if not f.startswith('.')]

recordings_folders = listdir(CUT_DIR + '/')
recordings_folders.sort()

for folder in recordings_folders:

    folder_files = listdir(CUT_DIR + '/' + folder + '/')
    create_directory(SPECTROGRAM_PATH + '/' + folder + '/')

    number_of_images = len(folder_files)
    for i, file in enumerate(folder_files):
        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))
        # read in a wav file
        sample_rate, data = wavfile.read(
            CUT_DIR + '/' + folder + '/' + file
        )
        # mono wav file
        samples = data.shape[0]

        # Create Figure and Axes instances
        fig = plt.figure(frameon=False)
        # 20 x 480 pixels
        fig.set_size_inches(0.2, 4.8)

        # save fig with only spectogram content
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)

        f, t, Sxx = spectrogram(data, sample_rate)
        dBS = 10 * np.log10(Sxx)  # convert to dB

        # 30 do is like Quiet rural area
        # 10 db is like Breathing.
        CUTOFF_THRESHOLD_DB = 25

        # all values below threshold are set to 0 db
        dBS[dBS < CUTOFF_THRESHOLD_DB] = 0

        plt.pcolormesh(t, f, dBS)
        plt.ylim(0, 3000)

        # remove .wav
        image_name = file[:-4]

        plt.savefig(
            SPECTROGRAM_PATH + '/' +
            folder + '/' + file[:-4] + '.jpg'
        )
        plt.close()
