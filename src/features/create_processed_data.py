# -*- coding: utf-8 -*-
import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import ML_MODELS, RAW_DATA_DIR, CUT_DIR, \
    AMPLITUDE_ARRAY_PATH, UNFILTERED_PATH


for i, model in enumerate(ML_MODELS):
    print("Processing %d/%d\n" % (i + 1, len(ML_MODELS)))

    print("Cutting recordings %d/%d\n" % (i + 1, len(ML_MODELS)))
    p_cut = subprocess.check_call(
        ['python', 'cut_original_recordings.py', '10', model['name'], RAW_DATA_DIR]
    )

    if model['voice_type'] == 'poly':
        print("Leveling combined recordings %d/%d\n" % (i + 1, len(ML_MODELS)))
        p_level = subprocess.check_call(
            ['python', 'level_combined_recordings.py',
                os.path.join(CUT_DIR, model['name'])]
        )
    print(p_level)
    is_random_forest = (model['model_type'] == 'rf')
    data_source = None
    if model['unfiltered']:
        print("Making unfiltered data %d/%d\n" % (i + 1, len(ML_MODELS)))
        p_unfilter = subprocess.check_call(
            ['python', 'make_unfiltered_data.py',
             model['name'], CUT_DIR, UNFILTERED_PATH, str(is_random_forest)]
        )
        print(p_unfilter)
        data_source = UNFILTERED_PATH
    else:
        print("Making amplitude array data %d/%d\n" % (i + 1, len(ML_MODELS)))
        # pdb.set_trace()
        is_random_forest = (model['model_type'] == 'rf')
        p_amplitude = subprocess.check_call(
            ['python', 'make_amplitude_array.py',
             model['name'], CUT_DIR, AMPLITUDE_ARRAY_PATH, str(is_random_forest)]
        )
        print(p_amplitude)
        data_source = AMPLITUDE_ARRAY_PATH

    if not data_source:
        print("Data source could not be found.")

    print("Creating train and test data %d/%d\n" % (i + 1, len(ML_MODELS)))
    processed_dir = os.path.join(data_source, model['name'])
    p_create = subprocess.check_call(
        ['python', 'create_train_test_data.py',
         processed_dir, str(model['unfiltered']), str(is_random_forest), model['name']]
    )
    print(p_create)
