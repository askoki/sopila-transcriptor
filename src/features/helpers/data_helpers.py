import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..', '..'))
from settings import FIGURES_DIR, AMPLITUDE_ARRAY_PATH, \
    PROCESSED_DATA_DIR, STATISTICS_DIR

import re
import itertools
import h5py
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


def natural_sort(l):
    '''
    needed in order to sort numbers and strings
    '''
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def plot_model_statistics(title, train_score, test_score, data_name):
    '''
    title -> string reporesenting figure title
    train -> list of keras values during n epoch on the training set
    valid -> list of keras values during n epoch on the validation set
    data_name -> string describing title
    '''
    # summarize history for accuracy
    plt.figure(title.capitalize())
    plt.bar([0, 1], [train_score, test_score])
    plt.xticks([0, 1], ('train', 'test'))
    plt.title('model %s' % (title.lower()))
    plt.ylim(0, 1)

    train_label = "%.4g%%" % (train_score * 100)
    plt.text(
        0,
        0.5,
        train_label,
        fontweight='bold',
        horizontalalignment='center',
        verticalalignment='center'
    )

    test_label = "%.4g%%" % (test_score * 100)
    plt.text(
        1,
        0.5,
        test_label,
        fontweight='bold',
        horizontalalignment='center',
        verticalalignment='center'
    )

    img_name = 'train_test_' + title.lower() + '_' + data_name + '.png'

    plt.savefig(
        os.path.join(FIGURES_DIR, img_name),
        format='png',
        dpi=300
    )
    plt.close()


def calculate_f1(precision, recall):
    if precision + recall == 0:
        return None
    return (2 * precision * recall) / (precision + recall)


def write_model_statistics(title, metrics_dict, training_shape, test_shape, parameters):
    """
    title -> string reporesenting name of the model
    metrics_dict -> dict containing accuracy, precision and recall metrics
    training_shape, test_shape -> tuple containing training and test data size
    parameters -> dict containing tested parameters in and iteration
    """
    with open(os.path.join(STATISTICS_DIR, title + '.txt'), 'w+') as f:
        print('n_estimators ' + str(parameters[0]), file=f)
        print('criterion ' + str(parameters[1]), file=f)
        print('bootstrap ' + str(parameters[2]), file=f)
        print('min_samples_split ' + str(parameters[3]), file=f)
        print('min_samples_leaf ' + str(parameters[4]), file=f)
        print('max_features ' + str(parameters[5]), file=f)
        print('max_depth ' + str(parameters[6]), file=f)

        print('Training_shape ' + str(training_shape.shape), file=f)
        print('Test_shape ' + str(test_shape.shape), file=f)
        print('Training_accuracy ' + str(metrics_dict['acc_train']), file=f)
        print('Training_precision ' +
              str(metrics_dict['precision_train']), file=f)
        print('Training_recall ' + str(metrics_dict['recall_train']), file=f)
        print('Training_F1 ' + str(calculate_f1(
            metrics_dict['precision_train'],
            metrics_dict['recall_train'])), file=f
        )
        print('Test_accuracy ' + str(metrics_dict['acc_test']), file=f)
        print('Test_precision ' +
              str(metrics_dict['precision_test']), file=f)
        print('Test_recall ' + str(metrics_dict['recall_test']), file=f)
        print('Test_F1 ' + str(calculate_f1(
            metrics_dict['precision_test'],
            metrics_dict['recall_test'])), file=f
        )


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

    # Create Figure and Axes instances
    fig = plt.figure("Confusion matrix", frameon=False)
    # 20 x 480 pixels
    fig.set_size_inches(20, 20)

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


def get_random_forest_data(dir_path=AMPLITUDE_ARRAY_PATH):
    """
    Returns tuple containing list of all amlitudes (X) and all_labels (y)
    """
    all_values = []
    all_labels = []
    array_size = get_min_data_size()
    for array_file in os.listdir(dir_path):
        file = h5py.File(os.path.join(dir_path, array_file), 'r')

        if dir_path != AMPLITUDE_ARRAY_PATH:
            values = file['waveform'].value[:array_size]
        else:
            values = file['amplitudes'].value[:array_size]
        labels = file['labels'].value[:array_size]
        # # m * n matrix
        all_values.extend(values)
        # # m * 1 vector
        all_labels.extend(labels)
        file.close()
    return (all_values, all_labels)


def get_train_data():
    file = h5py.File(os.path.join(
        PROCESSED_DATA_DIR, 'processed_data.hdf5'), 'r')

    return (
        file['x_train'].value,
        file['y_train'].value,
    )


def get_test_data():
    file = h5py.File(os.path.join(
        PROCESSED_DATA_DIR, 'processed_data.hdf5'), 'r')

    return (
        file['x_test'].value,
        file['y_test'].value,
    )
