#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py 'alternative'

# 2. step make spectrogram images from cut recordings
echo '2. Making spectrogram images from cut recordings...'
python make_spectrogram.py 'alternative'

# 4. apply filter to the images
echo '4. Applying filter to the images...'
python apply_filter.py 'alternative'

