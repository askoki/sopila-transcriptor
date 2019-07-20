#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py 10

# 2. level combined recordings
echo '2. Leveling stereo recordings'
python level_combined_recordings.py

# 3. Extract amplitudes from every cut recording
echo '3. Making file with all extracted amplitudes...'
python make_amplitude_array.py

# 4. distribute images to training and test set in processed data folder
echo '4. Creating training, validation and test set...'
python sort_train_validation_test_data.py

# # train
# python ../models/train_model.py
# # predict
# python ../models/predict_model.py

