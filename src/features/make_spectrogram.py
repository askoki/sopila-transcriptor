#!/usr/bin/env python
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import RAW_DATA_DIR, SPECTROGRAM_PATH
from scipy.signal import stft, spectrogram
from scipy.io import wavfile
from os import listdir

import matplotlib.pyplot as plt
import numpy as np
import wave
import pylab

# remove hidden files
recordings_folders = [f for f in listdir(RAW_DATA_DIR) if not f.startswith('.')]
recordings_folders.sort()

for folder in recordings_folders:
    folder_files = listdir(RAW_DATA_DIR + folder + '/')
    for file in folder_files:
        # read in a wav file
        sample_rate, data = wavfile.read(RAW_DATA_DIR + folder + '/' + file)
        # mono wav file
        samples = data.shape[0]

        # f, t, Zxx = stft(data, sample_rate)

        # Create Figure and Axes instances
        fig = plt.figure(frameon=False)
        # 500 x 500 pixels
        # fig.set_size_inches(5, 5)

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
