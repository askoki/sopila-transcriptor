#!/bin/sh

# 1. step cut recordings
echo '1. Cutting recordings'
python cut_original_recordings.py 'alternative'

# 2. Extract amplitudes from every cut recording
echo '2. Making file with all extracted amplitudes...'
python make_amplitude_array.py 'alternative'

