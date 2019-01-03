import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from helpers.file_helpers import create_directory, clear_dir
from pydub import AudioSegment
from os import listdir

# pass number of ms in a timeframe (10, 20, 25, 50)
if not len(sys.argv) > 1:
    step = 25
else:
    step = int(sys.argv[1])

# alternative dir
if len(sys.argv) > 2:
    from settings import REAL_DATA_RAW as RAW_DATA_DIR, REAL_DATA_CUT as CUT_DIR
else:
    from settings import RAW_DATA_DIR, CUT_DIR

clear_dir(CUT_DIR)

models_folders = listdir(RAW_DATA_DIR)
models_folders.sort()

for model in models_folders:

    recordings_folders = listdir(RAW_DATA_DIR + model + '/')
    recordings_folders.sort()

    for folder in recordings_folders:

        folder_files = listdir(RAW_DATA_DIR + model + '/' + folder + '/')

        create_directory(CUT_DIR + model + '/' + folder + '/')

        numeration = 0
        for file in folder_files:
            start = 0
            # in miliseconds
            title = str(step) + "ms"

            audioFile = AudioSegment.from_wav(
                RAW_DATA_DIR + model + '/' + folder + '/' + file)

            # measured in miliseconds
            duration = len(audioFile)
            number_of_segments = int(duration / step)

            for i in range(0, number_of_segments):
                end = start + step
                newAudio = audioFile[start:end]
                filepath = CUT_DIR + model + '/' + folder + \
                    '/' + title + str(numeration) + '.wav'
                newAudio.export(filepath, format="wav")
                start += step
                numeration += 1
