import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
from settings import ML_MODELS


for i, model in enumerate(ML_MODELS):
    print("Training %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'rf':
        continue
    
    string_parameters = '['
    split_string = model['best_params'].split('_')
    string_parameters += ','.join(split_string)
    string_parameters += ']'
    
    p = subprocess.check_call(
        ['python', 'train_rf_model.py',
         model['name'], string_parameters, 'True']
    )
    print(p)
