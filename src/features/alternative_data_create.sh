#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py 10 'alternative'

# 2. level combined recordings
echo '2. Leveling stereo recordings'
python level_combined_recordings.py 'alternative'

# 3. Extract amplitudes from every cut recording
echo '3. Making file with all extracted amplitudes...'
python make_amplitude_array.py 'alternative'

