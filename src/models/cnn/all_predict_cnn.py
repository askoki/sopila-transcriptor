import os
import sys
import subprocess
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
from settings import ML_MODELS


for i, model in enumerate(ML_MODELS):
    print("Predicting %d/%d\n" % (i + 1, len(ML_MODELS)))

    if model['model_type'] != 'cnn':
        continue

    num_classes = 13 if model['voice_type'] == 'mono' else 49
    p = subprocess.check_call(
        ['python', 'predict_rf_model.py', model['name'],
         model['best_params'], str(num_classes), str(model['unfiltered'])]
    )
    print(p)
