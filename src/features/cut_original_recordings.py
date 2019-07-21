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

if not sys.argv[2]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[2])

if not sys.argv[3]:
    print('Enter path of raw data dir')
    sys.exit()

RAW_DATA_DIR = str(sys.argv[3])

if not sys.argv[4]:
    print('Enter path of cut dir')
    sys.exit()

CUT_DIR = str(sys.argv[4])


def cut_folder_files(folder):
    folder_files = listdir(os.path.join(RAW_DATA_DIR, ML_MODEL, folder))
    create_directory(os.path.join(CUT_DIR, ML_MODEL, folder))

    numeration = 0
    for file in folder_files:
        start = 0
        # in miliseconds
        title = str(step) + "ms"
        audio_file = AudioSegment.from_wav(
            os.path.join(RAW_DATA_DIR, ML_MODEL, folder, file)
        )

        # measured in miliseconds
        duration = len(audio_file)
        number_of_segments = int(duration / step)

        for i in range(0, number_of_segments):
            end = start + step
            new_audio = audio_file[start:end]

            file_path = os.path.join(
                CUT_DIR, ML_MODEL, folder, title + str(numeration) + '.wav'
            )
            new_audio.export(file_path, format="wav")
            start += step
            numeration += 1

# -------- PARALLELIZE ----------
from multiprocessing import Pool


if __name__ == '__main__':
    clear_dir(os.path.join(CUT_DIR, ML_MODEL))

    recordings_folders = listdir(os.path.join(RAW_DATA_DIR, ML_MODEL))
    recordings_folders.sort()
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(cut_folder_files, recordings_folders)
