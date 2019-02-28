import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import MODEL_DIR
from joblib import load
# from features.helpers.file_helpers import save_list_to_file
from features.helpers.data_helpers import natural_sort, plot_confusion_matrix
from features.helpers.data_helpers import get_test_data
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import PCA


# provide model name
if len(sys.argv) < 2:
    model_name = 'silece_lower_random_forest_default_name'
    matrix_name = 'silece_lower_matrix_default_random_forest'
else:
    model_name = str(sys.argv[1]) + '_random_forest'
    matrix_name = sys.argv[2] + '_random_forest'

class_labels = [
    'm0', 'm1', 'm2', 'm3', 'm4', 'm5',
    'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'blank',
]

x_test, y_test = get_test_data()
rnd_clf = load(os.path.join(MODEL_DIR, model_name + '.joblib'))

y_predicted = rnd_clf.predict(x_test)

cm = confusion_matrix(y_test, y_predicted)
plot_confusion_matrix(cm, class_labels, matrix_name)
