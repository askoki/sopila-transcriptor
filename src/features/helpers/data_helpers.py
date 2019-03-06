import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..', '..'))
from settings import FIGURES_DIR, AMPLITUDE_ARRAY_PATH, PROCESSED_DATA_DIR

import re
import itertools
import h5py
import numpy as np
import matplotlib.pyplot as plt


def natural_sort(l):
    '''
    needed in order to sort numbers and strings
    '''
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def plot_model_statistics(title, train, valid, data_name):
    '''
    title -> string reporesenting figure title
    train -> list of keras values during n epoch on the training set
    valid -> list of keras values during n epoch on the validation set
    data_name -> string describing title
    '''
    # summarize history for accuracy
    plt.figure(title.capitalize())
    plt.plot(train)
    plt.plot(valid)
    plt.title('model %s' % (title.lower()))
    plt.ylabel(title.lower())
    plt.xlabel('epoch')

    plt.legend(['train', 'validation'], loc='upper left')

    img_name = title.lower() + '_' + data_name + '.png'

    plt.savefig(os.path.join(FIGURES_DIR, img_name), format='png', dpi=300)
    plt.close()


def plot_confusion_matrix(cm, classes, matrix_name, normalize=False, title='', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.

    Code is taken from scikit-learn.org example.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.figure("Confusion matrix")
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(
            j, i,
            format(cm[i, j], fmt),
            horizontalalignment="center",
            color="white" if cm[i, j] > thresh else "black"
        )

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    plt.savefig(
        os.path.join(FIGURES_DIR, 'confusion_matrix_' + matrix_name + '.png'),
        format='png',
        dpi=300
    )
    plt.close()
    
    
def get_min_data_size():
    '''
    Returns size of matrix with lowest size (needed for balanced dataset)
    '''
    min_value = sys.maxsize
    for array_file in os.listdir(AMPLITUDE_ARRAY_PATH):
        file = h5py.File(os.path.join(AMPLITUDE_ARRAY_PATH, array_file), 'r')
        if file['amplitudes'].shape[0] < min_value:
            min_value = file['amplitudes'].shape[0]
        file.close()
    return min_value


def get_random_forest_data():
    '''
    Returns tuple containing list of all amplitudes (X) and all_labels (y)
    '''
    all_amplitudes = []
    all_labels = []
    array_size = get_min_data_size()
    for array_file in os.listdir(AMPLITUDE_ARRAY_PATH):
        file = h5py.File(os.path.join(AMPLITUDE_ARRAY_PATH, array_file), 'r')

        values = file['amplitudes'].value[:array_size]
        labels = file['labels'].value[:array_size]
        # # m * n matrix
        all_amplitudes.extend(values)
        # # m * 1 vector
        all_labels.extend(labels)
        file.close()
    return (all_amplitudes, all_labels)


def get_train_data():
    file = h5py.File(os.path.join(PROCESSED_DATA_DIR, 'processed_data.hdf5'), 'r')

    return (
        file['x_train'].value,
        file['y_train'].value,
    )
    

def get_test_data():
    file = h5py.File(os.path.join(PROCESSED_DATA_DIR, 'processed_data.hdf5'), 'r')

    return (
        file['x_test'].value,
        file['y_test'].value,
    )
