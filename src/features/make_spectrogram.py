#!/usr/bin/env python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import CUT_DIR, SPECTROGRAM_PATH
from helpers.file_helpers import create_directory, clear_dir
from scipy.signal import stft, spectrogram
from scipy.io import wavfile
from os import listdir

import matplotlib.pyplot as plt
import numpy as np
import wave
import pylab

# delete old spectrogram data (if exists)
clear_dir(SPECTROGRAM_PATH)

# remove hidden files
recordings_folders = [f for f in listdir(CUT_DIR) if not f.startswith('.')]
recordings_folders.sort()

for folder in recordings_folders:
    folder_files = listdir(CUT_DIR + folder + '/')

    create_directory(SPECTROGRAM_PATH + folder + '/')
    for file in folder_files:
        # read in a wav file
        sample_rate, data = wavfile.read(CUT_DIR + folder + '/' + file)
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
        plt.pcolormesh(t, f, dBS)

        plt.ylim(0, 3000)

        # remove .wav
        image_name = file[:-4]
        plt.savefig(SPECTROGRAM_PATH + folder + '/' + file[:-4] + '.jpg')
