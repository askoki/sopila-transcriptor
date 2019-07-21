import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
from settings import ML_MODELS


for i, model in enumerate(ML_MODELS):
    print("Predicting %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'rf':
        continue

    p = subprocess.check_call(
        ['python', 'predict_rf_model.py',
         model['name'], model['best_params'], model['unfiltered']]
    )
    print(p)
