#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py

# 2. step make spectrogram images from cut recordings
echo '2. Making spectrogram images from cut recordings...'
python make_spectrogram.py

# 3. make filter (if it does not exist)
echo '3. Making filter...'
python ../utils/make_filter.py

# 4. apply filter to the images
echo '4. Applying filter to the images...'
python apply_filter.py

# 5. distribute images to training and test set in processed data folder
echo '5. Creating training, validation and test set...'
python sort_train_validation_test_data.py

