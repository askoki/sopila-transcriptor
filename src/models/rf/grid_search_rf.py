import os
import sys
import subprocess
from itertools import product
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
from settings import ML_MODELS

for i, model in enumerate(ML_MODELS):
    print("Training %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'rf':
        continue

    criterion = ['gini', 'entropy']
    bootstrap = [False]
    min_samples_split = [2, 4, 6]
    min_samples_leaf = [1]
    max_features = ['auto']

    if model['voice_type'] == 'mono' and not model['unfiltered']:
        # rf 13 classes
        n_estimators = [110, 150, 170]
        max_depth = [90, 110, 130]
    else:
        # rf 49 classes and rf 13 classes no filter
        n_estimators = [800, 900, 1000]
        max_depth = [60, 80, 100]

    param_cartesian_product = product(
        n_estimators,
        criterion,
        min_samples_split,
        min_samples_leaf,
        max_features,
        max_depth,
        bootstrap
    )

    for i, parameters in enumerate(param_cartesian_product):
        print(parameters)

        list_to_string = '['
        for j in range(len(parameters)):
            list_to_string += str(parameters[j]) + ','
        list_to_string = list_to_string[:-1]
        list_to_string += ']'

        p = subprocess.check_call(
            ['python', 'train_rf_model.py',
             model['name'], list_to_string, 'False']
        )
        print(p)
