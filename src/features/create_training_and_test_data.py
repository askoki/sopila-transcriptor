import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import TRAINING_DIR, TEST_DIR, CUT_DIR
from os import listdir, remove
from shutil import copy2
from random import shuffle


for path in [TRAINING_DIR, TEST_DIR]:
    folders = listdir(path)
    folders.sort()

    for folder in folders:
        folder_files = listdir(path + folder + "/")
        for filename in folder_files:
            remove(path + folder + "/" + filename)

folders = listdir(path)
folders.sort()

training_volume = 0.8

for folder in folders:
    folder_files = listdir(CUT_DIR + folder + "/")
    # randomize data
    for i in range(100):
        shuffle(folder_files)

    split_index = int(training_volume * len(folder_files))

    training_files = folder_files[:split_index]
    for filename in training_files:
        copy2(CUT_DIR + folder + "/" + filename, TRAINING_DIR + folder + "/" + filename)

    test_files = folder_files[split_index:]
    for filename in test_files:
        copy2(CUT_DIR + folder + "/" + filename, TEST_DIR + folder + "/" + filename)
