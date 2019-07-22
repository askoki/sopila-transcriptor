import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
from settings import ML_MODELS


for i, model in enumerate(ML_MODELS):
    print("Training %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'cnn':
        continue

    string_parameters = '['
    split_string = model['best_params'].split('_')
    string_parameters += ','.join(split_string)
    string_parameters += ']'

    num_classes = 13 if model['voice_type'] == 'mono' else 49
    p = subprocess.check_call(
        ['python', 'train_cnn_model.py',
         model['name'], string_parameters, 'True', str(num_classes)]
    )
    print(p)
