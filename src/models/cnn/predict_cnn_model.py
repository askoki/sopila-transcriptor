import os
import sys
import h5py
import keras
import numpy as np
from keras_metrics import precision, recall
from keras.models import model_from_json
from sklearn.metrics import accuracy_score, confusion_matrix, \
    precision_score, recall_score
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import MODEL_DIR, CUT_DIR, REAL_DATA_AMP, \
    REAL_DATA_UNFILTERED, REAL_DATA_PREDICTIONS, STATISTICS_DIR
from features.helpers.data_helpers import plot_confusion_matrix, get_test_data, \
    write_acc_prec_recall_f1


if not sys.argv[1]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[1])

if not sys.argv[2]:
    print(
        'Enter training parameters in the following order: cnn_layers, \
        num_filters, filter_size, hidden_layers'
    )
    sys.exit()

parameters = sys.argv[2].split('_')
parameters = [int(i) for i in parameters]
model_name = ML_MODEL + '_' + str(sys.argv[2])

if not sys.argv[3]:
    print('Enter number of classes of a model')
    sys.exit()

num_classes = int(sys.argv[3])

if not sys.argv[4]:
    print('Enter boolean "True" if models uses unfiltered data')
    sys.exit()

is_unfiltered = (sys.argv[4] == 'True')

# dimensions of our images
img_height, img_width = 640, 480
input_shape = (img_height, img_width, 3)

# use test set
x_test, y_test = get_test_data(ML_MODEL)

n_rows, n_cols = x_test.shape

batch_size = 1000

class_labels = os.listdir(os.path.join(CUT_DIR, ML_MODEL))
class_labels.sort()
class_labels = [
    label.replace('vv_', '').replace(
        'silence', 'blank') for label in class_labels
]

x_test = np.expand_dims(x_test, axis=3)

# load the model we saved
with open(os.path.join(MODEL_DIR, ML_MODEL, 'model_' + model_name + '.json'), 'r') as f:
    model = model_from_json(f.read())

# load the model weights
model.load_weights(os.path.join(MODEL_DIR, ML_MODEL, 'model_' + model_name + '.h5'))
model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy', precision(), recall()]
)

true_classes = y_test

predicted_classes = model.predict(x_test, batch_size=20)
predicted_classes = np.argmax(predicted_classes, axis=1)

test_accuracy = accuracy_score(predicted_classes, true_classes)
test_precision = precision_score(
    true_classes, predicted_classes, average='micro')
test_recall = recall_score(true_classes, predicted_classes, average='micro')

metrics_dict = {
    'acc_test': test_accuracy,
    'precision_test': test_precision,
    'recall_test': test_recall
}
print(metrics_dict)

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


cm = confusion_matrix(true_classes, predicted_classes)
plot_confusion_matrix(cm, class_labels, model_name, ML_MODEL)

# ------ real data predict -------

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

    to_be_predicted = np.expand_dims(features, axis=3)
    # predicted class
    predicted_classes = model.predict(to_be_predicted, batch_size=20)
    predicted_classes = np.argmax(predicted_classes, axis=1)
    file.close()

    predicted_file = h5py.File(os.path.join(
        REAL_DATA_PREDICTIONS, ML_MODEL, filename), 'w'
    )
    predicted_file.create_dataset(
        'predictions',
        data=predicted_classes,
        dtype='i'
    )
    predicted_file.close()
