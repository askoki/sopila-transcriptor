import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from pydub import AudioSegment
from settings import NUMBER_OF_CORES
from os import listdir

# pass number of ms in a timeframe (10, 20, 25, 50)
if not len(sys.argv) > 1:
    step = 10
else:
    step = int(sys.argv[1])

# alternative dir
if len(sys.argv) > 2:
    from settings import REAL_DATA_RAW as RAW_DATA_DIR, REAL_DATA_CUT as CUT_DIR
else:
    from settings import RAW_DATA_DIR, CUT_DIR


def cut_folder_files(folder):
    folder_files = listdir(os.path.join(RAW_DATA_DIR, folder))
    create_directory(os.path.join(CUT_DIR, folder))

    numeration = 0
    for file in folder_files:
        start = 0
        # in miliseconds
        title = str(step) + "ms"
        audioFile = AudioSegment.from_wav(
            os.path.join(RAW_DATA_DIR, folder, file)
        )

        # measured in miliseconds
        duration = len(audioFile)
        number_of_segments = int(duration / step)

        for i in range(0, number_of_segments):
            end = start + step
            newAudio = audioFile[start:end]

            filepath = os.path.join(
                CUT_DIR, folder, title + str(numeration) + '.wav'
            )
            newAudio.export(filepath, format="wav")
            start += step
            numeration += 1

# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    clear_dir(os.path.join(CUT_DIR))

    recordings_folders = listdir(os.path.join(RAW_DATA_DIR))
    recordings_folders.sort()
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(cut_folder_files, recordings_folders)
