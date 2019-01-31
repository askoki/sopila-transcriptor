import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from pydub import AudioSegment
from settings import NUMBER_OF_CORES
from os import listdir
from settings import CUT_DIR


def level_recordings(folder):
    folder_files = listdir(os.path.join(CUT_DIR, folder))

    number_of_images = len(folder_files)
    for i, file in enumerate(folder_files):
        # print progress
        print('\rFolder: %s %d/%d\r' % (folder, i, number_of_images))

        # read in a wav file
        data = AudioSegment.from_file(os.path.join(CUT_DIR, folder, file), format='wav')
        
        # skip non stereo (combined) files
        if data.channels <= 1:
            # skip whole folder
            return

        left, right = data.split_to_mono()
        diff = abs(left.dBFS - right.dBFS)
        
        # compare left and right channel in dBFS
        get_gain = lambda l_ch, r_ch: 0 if l_ch > r_ch else diff
        
        left = left.apply_gain(get_gain(left.dBFS, right.dBFS))
        right = right.apply_gain(get_gain(right.dBFS, left.dBFS))
        
        data = left.overlay(right)
        data.export(os.path.join(CUT_DIR, folder, file), format='wav')
        

# -------- PARALLELIZE ----------
from multiprocessing import Pool

if __name__ == '__main__':
    recordings_folders = listdir(os.path.join(CUT_DIR))
    recordings_folders.sort()
    with Pool(processes=NUMBER_OF_CORES) as pool:
        pool.map(level_recordings, recordings_folders)
