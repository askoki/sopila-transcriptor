import os
import sys
import re
import itertools
import h5py
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(sys.path[0], '..', '..'))
from settings import FIGURES_DIR, PROCESSED_DATA_DIR, \
    CUT_DIR, STATISTICS_DIR


def natural_sort(l):
    """
    needed in order to sort numbers and strings
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def calculate_f1(precision, recall):
    if precision + recall == 0:
        return None
    return (2 * precision * recall) / (precision + recall)


def write_model_statistics(title, history_dict, input_shape, validation_split, parameters):
    """
    title -> string reporesenting name of the model
    history_dict -> keras dictionary containing model statistics
    input_shape -> tuple containing training data size
    validation_split -> float describing training - validation split
    parameters -> dict containing tested parameters in and iteration
    """
    with open(os.path.join(STATISTICS_DIR, title + '.txt'), 'w+') as f:
        validation_num = int(input_shape[0] * validation_split)
        training_num = int(input_shape[0] - validation_num)
        print('Cnn_layers ' + str(parameters[0]), file=f)
        print('Num_filters ' + str(parameters[1]), file=f)
        print('Filter_size ' + str(parameters[2]), file=f)
        print('Hidden_layers ' + str(parameters[3]), file=f)

        print('Input_shape ' + str(input_shape), file=f)
        print('Training_data ' + str(training_num), file=f)
        print('Validation_data ' + str(validation_num), file=f)
        print('Training_accuracy ' + str(history_dict['acc'][0]), file=f)
        print('Training_precision ' +
              str(history_dict['precision'][0]), file=f)
        print('Training_recall ' + str(history_dict['recall'][0]), file=f)
        print('Training_F1 ' + str(calculate_f1(
            history_dict['precision'][0],
            history_dict['recall'][0])), file=f
        )
        print('Validation_accuracy ' + str(history_dict['val_acc'][0]), file=f)
        print('Validation_precision ' +
              str(history_dict['val_precision'][0]), file=f)
        print('Validation_recall ' +
              str(history_dict['val_recall'][0]), file=f)
        print('Validation_F1 ' + str(calculate_f1(
            history_dict['val_precision'][0],
            history_dict['val_recall'][0])), file=f
        )


def plot_model_statistics(title, train, valid, data_name):
    """
    title -> string reporesenting figure title
    train -> list of keras values during n epoch on the training set
    valid -> list of keras values during n epoch on the validation set
    data_name -> string describing title
    """
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

    fig = plt.figure("Confusion matrix")
    fig.set_size_inches(22, 22)

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
        dpi=500
    )
    plt.close()


def get_min_data_size(data_path, is_unfiltered):
    """
    data_path -> Path to the processed (but not splitted) data
    is_unfiltered -> boolean value determining weather data 
    was preprocessed or not

    Returns size of matrix with lowest size (needed for balanced dataset)
    """
    min_value = sys.maxsize

    dict_key = 'waveform' if is_unfiltered else 'amplitudes'
    for array_file in os.listdir(data_path):
        file = h5py.File(os.path.join(data_path, array_file), 'r')
        dict_obj = file['waveform'] if is_unfiltered else file['amplitudes']
        if dict_obj.shape[0] < min_value:
            min_value = dict_obj.shape[0]
        file.close()
    return min_value


def get_data(data_path, is_unfiltered):
    """
    data_path -> Path to the processed (but not splitted) data
    is_unfiltered -> boolean value determining weather data 
    was preprocessed or not

    Returns tuple containing list of all amlitudes (X) and all_labels (y)
    """
    all_values = []
    all_labels = []
    array_size = get_min_data_size(data_path, is_unfiltered)
    for array_file in os.listdir(data_path):
        file = h5py.File(os.path.join(data_path, array_file), 'r')

        if is_unfiltered:
            values = file['waveform'].value[:array_size]
        else:
            values = file['amplitudes'].value[:array_size]
        labels = file['labels'].value[:array_size]

        # m * n matrix
        all_values.extend(values)

        # m * 1 vector
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


def get_folder_class_index(folder_name):

    class_labels = os.listdir(CUT_DIR)
    class_labels.sort()

    try:
        return_class = class_labels.index(folder_name)
    except ValueError:
        print("Class was not found")
        return_class = 0
    return return_class
