#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py 10

# 2. Extract amplitudes from every cut recording
echo '2. Making file with all extracted amplitudes...'
python make_amplitude_array.py
# python make_unfiltered_data.py

# 3. Split data set into training and test
echo '3. Creating training and test set...'
python create_train_test_data.py

