import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import MODEL_DIR, CUT_DIR, REAL_DATA_AMP, REAL_DATA_PREDICTIONS
from joblib import load
import h5py
from features.helpers.data_helpers import natural_sort, plot_confusion_matrix
from features.helpers.data_helpers import get_test_data
from sklearn.metrics import confusion_matrix


if len(sys.argv) < 2:
    model_name = '49_class_random_forest_default_name'
    matrix_name = '49_class_matrix_default_random_forest'
else:
    model_name = str(sys.argv[1]) + '_random_forest'
    matrix_name = sys.argv[2]

class_labels = os.listdir(CUT_DIR)
class_labels.sort()
class_labels = [label.replace('vv_', '').replace('silence', 'blank') for label in class_labels]

x_test, y_test = get_test_data()
rnd_clf = load(os.path.join(MODEL_DIR, model_name + '.joblib'))

y_predicted = rnd_clf.predict(x_test)

cm = confusion_matrix(y_test, y_predicted)
plot_confusion_matrix(cm, class_labels, matrix_name)

print("Predicting real data (must be created first)")
for filename in os.listdir(REAL_DATA_AMP):
    file = h5py.File(os.path.join(REAL_DATA_AMP, filename), 'r')
    y_predicted = rnd_clf.predict(file['amplitudes'].value)
    file.close()

    predicted_file = h5py.File(os.path.join(REAL_DATA_PREDICTIONS, filename), 'w')
    dt = h5py.special_dtype(vlen=str)
    predicted_file.create_dataset(
        'predictions',
        data=y_predicted,
        dtype=dt
    )
    predicted_file.close()
