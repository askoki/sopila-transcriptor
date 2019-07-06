import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..',))

# from joblib import dump, load
from joblib import dump
from settings import MODEL_DIR, USE_GPU
from joblib import load
from features.helpers.data_helpers import plot_model_statistics, \
    get_train_data, get_test_data, write_model_statistics
import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score
from itertools import product

if USE_GPU:
    # use if you are running on a PC with many GPU-s
    # needs to be at the beginning of the file
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # the GPU id to use, usually either "0" or "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

if len(sys.argv) < 2:
    model_name = '49_class_random_forest_default_name'
else:
    model_name = str(sys.argv[1])


x_train, y_train = get_train_data()

# Kreiranje random forest klasifikatora
rnd_clf = RandomForestClassifier(
    n_estimators=100,
    criterion='gini',
    n_jobs=-1,
    verbose=2,
)

n_estimators = [110, 130, 150, 170, 190]
criterion = ['gini', 'entropy']
bootstrap = [False]
min_samples_split = [2, 4, 6]
min_samples_leaf = [1]
max_features = ['auto']
max_depth = [90, 100, 110, 120, 130]
bootstrap = [False]

param_cartesian_product = product(
    n_estimators,
    criterion,
    bootstrap,
    min_samples_split,
    min_samples_leaf,
    max_features,
    max_depth,
)

for parameters in param_cartesian_product:
    # Treniranje i predviđanje modela
    print('Before:')
    print(datetime.datetime.now())
    rnd_clf.fit(X=x_train, y=y_train)
    print('After:')
    print(datetime.datetime.now())
    dump(rnd_clf, os.path.join(MODEL_DIR, model_name + '.joblib'))

    x_test, y_test = get_test_data()

    y_predicted_training = rnd_clf.predict(x_train)
    train_accuracy = rnd_clf.score(X=x_train, y=y_train)
    train_precision = precision_score(
        y_train, y_predicted_training, average='micro')
    train_recall = recall_score(y_train, y_predicted_training, average='micro')

    y_predicted = rnd_clf.predict(x_test)
    test_accuracy = rnd_clf.score(X=x_test, y=y_test)
    test_precision = precision_score(y_test, y_predicted, average='micro')
    test_recall = recall_score(y_test, y_predicted, average='micro')

    metrics_dict = {
        'acc_train': train_accuracy,
        'precision_train': train_precision,
        'recall_train': train_recall,
        'acc_test': test_accuracy,
        'precision_test': test_precision,
        'recall_test': test_recall
    }

    name = model_name
    for i in range(7):
        name += '_' + str(parameters[i])

    write_model_statistics(
        name, metrics_dict, x_train, x_test, parameters
    )
    plot_model_statistics(
        'accuracy',
        train_accuracy,
        test_accuracy,
        name
    )

    print(train_accuracy)
    print(test_accuracy)
