import os
import sys
import h5py
from joblib import load
from sklearn.metrics import confusion_matrix, precision_score, recall_score
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import MODEL_DIR, CUT_DIR, REAL_DATA_AMP, REAL_DATA_PREDICTIONS, \
    REAL_DATA_UNFILTERED, STATISTICS_DIR
from features.helpers.data_helpers import plot_confusion_matrix, \
    write_acc_prec_recall_f1, get_test_data


if not sys.argv[1]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[1])

if not sys.argv[2]:
    print('Enter matrix name (parameters)')
    sys.exit()

model_name = ML_MODEL + '_' + str(sys.argv[2])


if not sys.argv[3]:
    print('Enter boolean "True" if models uses unfiltered data')
    sys.exit()

is_unfiltered = (sys.argv[3] == 'True')

class_labels = os.listdir(os.path.join(CUT_DIR, ML_MODEL))
class_labels.sort()

x_test, y_test = get_test_data(ML_MODEL)
rnd_clf = load(os.path.join(MODEL_DIR, ML_MODEL, model_name + '.joblib'))

y_predicted = rnd_clf.predict(x_test)

cm = confusion_matrix(y_test, y_predicted)
plot_confusion_matrix(cm, class_labels, model_name, ML_MODEL)

test_accuracy = rnd_clf.score(X=x_test, y=y_test)
test_precision = precision_score(y_test, y_predicted, average='macro')
test_recall = recall_score(y_test, y_predicted, average='macro')

metrics_dict = {
    'acc_test': test_accuracy,
    'precision_test': test_precision,
    'recall_test': test_recall
}

write_acc_prec_recall_f1(
    os.path.join(
        STATISTICS_DIR,
        ML_MODEL,
        'test_stats_%s.txt' % model_name
    ),
    metrics_dict,
    'Test',
    'test'
)


real_data_path = os.path.join(REAL_DATA_AMP, ML_MODEL)
if is_unfiltered:
    real_data_path = os.path.join(REAL_DATA_UNFILTERED, ML_MODEL)

print("Predicting real data (must be created first)")
for filename in os.listdir(real_data_path):
    file = h5py.File(os.path.join(real_data_path, filename), 'r')
    features = None

    if is_unfiltered:
        features = file['waveform'].value
    else:
        features = file['amplitudes'].value

    y_predicted = rnd_clf.predict(features)
    file.close()

    predicted_file = h5py.File(
        os.path.join(REAL_DATA_PREDICTIONS, ML_MODEL, filename), 'w'
    )
    dt = h5py.special_dtype(vlen=str)
    predicted_file.create_dataset(
        'predictions',
        data=y_predicted,
        dtype=dt
    )
    predicted_file.close()
