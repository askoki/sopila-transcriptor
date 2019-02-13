import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..',))

# from joblib import dump, load
from joblib import dump
import pandas as pd
from settings import MODEL_DIR, USE_GPU
from features.helpers.data_helpers import plot_model_statistics, \
    get_train_and_test_data
import datetime

from sklearn.ensemble import RandomForestClassifier

if USE_GPU:
    # use if you are running on a PC with many GPU-s
    # needs to be at the beginning of the file
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # the GPU id to use, usually either "0" or "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

if len(sys.argv) < 2:
    model_name = 'random_forest_default_name'
else:
    model_name = int(sys.argv[1])

x_train, x_test, y_train, y_test = get_train_and_test_data()

# Kreiranje random forest klasifikatora
rnd_clf = RandomForestClassifier(n_estimators=500, criterion='gini', n_jobs=-1)

# Treniranje i predviđanje modela
print('Before:')
print(datetime.datetime.now())
rnd_clf.fit(X=x_train, y=y_train)
print('After:')
print(datetime.datetime.now())
dump(rnd_clf, os.path.join(MODEL_DIR, model_name + '.joblib'))

print(rnd_clf.score(X=x_train, y=y_train))
print(rnd_clf.score(X=x_test, y=y_test))




