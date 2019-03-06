import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import MODEL_DIR

from model import get_model
from features.helpers.file_helpers import save_list_to_file
from features.helpers.data_helpers import plot_confusion_matrix, get_test_data
from sklearn.metrics import confusion_matrix

import keras
import numpy as np

# number of classes required argument
num_classes = int(sys.argv[1])

# provide model name
model_name = str(sys.argv[2])
matrix_name = sys.argv[3]

# dimensions of our images
img_height, img_width = 640, 480
input_shape = (img_height, img_width, 3)

# use test set
x_test, y_test = get_test_data()

n_rows, n_cols = x_test.shape

batch_size = 50

class_labels = [
    'm0', 'm1', 'm2', 'm3', 'm4', 'm5',
    'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'blank',
]

# model must be the same as trained
model = get_model((n_cols, 1), num_classes)

x_test = np.expand_dims(x_test, axis=3)

# load the model we saved
model.load_weights(os.path.join(MODEL_DIR, model_name + '.h5'))
model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy']
)

true_classes = y_test
predicted_classes = model.predict_classes(x_test, batch_size=20)

cm = confusion_matrix(true_classes, predicted_classes)
plot_confusion_matrix(cm, class_labels, matrix_name)

# ------ real data predict

from settings import REAL_DATA_AMP, REAL_DATA_PREDICTIONS
import h5py

audio_files = os.listdir(os.path.join(REAL_DATA_AMP))
audio_files.sort()
 
for filename in audio_files:
    file = h5py.File(os.path.join(REAL_DATA_AMP, filename), 'r')
    to_be_predicted = np.expand_dims(file['amplitudes'].value, axis=3)
    # predicted class
    predicted_classes = model.predict_classes(to_be_predicted, batch_size=20)
    file.close()

    predicted_file = h5py.File(os.path.join(REAL_DATA_PREDICTIONS, filename), 'w')
    predicted_file.create_dataset(
        'predictions',
        data=predicted_classes,
        dtype='i'
    )
    predicted_file.close()
