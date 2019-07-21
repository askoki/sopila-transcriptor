import os
import sys
import subprocess
from itertools import product
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
from settings import ML_MODELS
from features.data_helpers import list_to_string


for i, model in enumerate(ML_MODELS):
    print("Training %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'cnn':
        continue

    cnn_layers = [1, 2, 3]  # 4, 5
    num_filters = [16, 32, 64]  # 128
    filter_size = [3, 5, 7]
    hidden_layers = [64, 128]

    param_cartesian_product = product(
        cnn_layers,
        num_filters,
        filter_size,
        hidden_layers
    )

    for i, parameters in enumerate(param_cartesian_product):
        print(parameters)
        num_classes = 13 if model['voice_type'] == 'mono' else 49
        p = subprocess.check_call(
            ['python', 'train_rf_model.py', model['name'],
             list_to_string(parameters), 'False', str(num_classes)]
        )
        print(p)
