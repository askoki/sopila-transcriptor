import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from helpers.file_helpers import create_directory, clear_dir
from settings import RAW_DATA_DIR, CUT_DIR
from pydub import AudioSegment
from os import listdir

clear_dir(CUT_DIR)

recordings_folders = listdir(RAW_DATA_DIR)
recordings_folders.sort()

for folder in recordings_folders:

    folder_files = listdir(RAW_DATA_DIR + folder + '/')

    create_directory(CUT_DIR + folder + '/')
    numeration = 0
    for file in folder_files:
        start = 0
        # in miliseconds
        step = 50
        title = str(step) + "ms"

        audioFile = AudioSegment.from_wav(RAW_DATA_DIR + folder + "/" + file)

        # measured in miliseconds
        duration = len(audioFile)
        number_of_segments = int(duration / step)

        for i in range(0, number_of_segments):
            end = start + step
            newAudio = audioFile[start:end]
            newAudio.export(CUT_DIR + folder + '/' + title + str(numeration) + '.wav', format="wav")
            start += step
            numeration += 1
