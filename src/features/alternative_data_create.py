# -*- coding: utf-8 -*-
import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import REAL_DATA_RAW, REAL_DATA_CUT, \
    REAL_DATA_AMP, REAL_DATA_UNFILTERED, ML_MODELS


for i, model in enumerate(ML_MODELS):
    print("Processing %d/%d\n" % (i + 1, len(ML_MODELS)))

    print("Cutting recordings %d/%d\n" % (i + 1, len(ML_MODELS)))
    p_cut = subprocess.check_call(
        ['python', 'cut_original_recordings.py', '10',
            model['name'], REAL_DATA_RAW, REAL_DATA_CUT]
    )
    print(p_cut)

    if model['voice_type'] == 'poly':
        print("Leveling combined recordings %d/%d\n" % (i + 1, len(ML_MODELS)))
        p_level = subprocess.check_call(
            ['python', 'level_combined_recordings.py',
                os.path.join(REAL_DATA_CUT, model['name'])]
        )
        print(p_level)

    is_random_forest = (model['model_type'] == 'rf')
    if model['unfiltered']:
        print("Making unfiltered data %d/%d\n" % (i + 1, len(ML_MODELS)))
        p_unfilter = subprocess.check_call([
            'python',
            'make_unfiltered_data.py',
            model['name'],
            REAL_DATA_CUT,
            REAL_DATA_UNFILTERED,
            str(is_random_forest)
        ])
        print(p_unfilter)
    else:
        print("Making amplitude array data %d/%d\n" % (i + 1, len(ML_MODELS)))
        is_random_forest = (model['model_type'] == 'rf')
        p_amplitude = subprocess.check_call([
            'python',
            'make_amplitude_array.py',
            model['name'],
            REAL_DATA_CUT,
            REAL_DATA_AMP,
            str(is_random_forest)
        ])
        print(p_amplitude)
