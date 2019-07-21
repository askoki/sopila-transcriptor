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
from settings import FIGURES_DIR, PROCESSED_DATA_DIR, STATISTICS_DIR


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


def write_acc_prec_recall_f1(file_path, metrics_dict, label, dict_key):
    """
    file_path -> string describing path to the file
    metrics_dict -> dict containing accuracy, precision and recall metrics
    label -> Which label should be written in the file (Validation/Test)
    dict_key -> Which value should be used from the metrics_dict (val/test)
    """
    with open(file_path, 'w+') as f:
        print(
            label + '_accuracy ' + str(metrics_dict['acc_' + dict_key]),
            file=f
        )
        print(
            label + '_precision ' + str(metrics_dict['precision_' + dict_key]),
            file=f
        )
        print(
            label + '_recall ' + str(metrics_dict['recall_' + dict_key]),
            file=f
        )
        print(
            label + '_F1 ' + str(
                calculate_f1(
                    metrics_dict['precision_' + dict_key],
                    metrics_dict['recall_' + dict_key]
                )
            ), file=f
        )


def write_rf_model_statistics(title, metrics_dict, training_shape, validation_shape,
                              parameters, model_name, mode='val'):
    """
    title -> string reporesenting name of the model
    metrics_dict -> dict containing accuracy, precision and recall metrics
    training_shape, validation_shape -> tuple containing training and test data size
    parameters -> dict containing tested parameters in and iteration
    model_name -> name of the folder where statistics will be saved 
    (defined according to ML_MODELS in settings.py)
    mode -> determine the labels: validation or test
    """
    label = 'Validation' if mode == 'val' else 'test'
    dict_key = 'val' if mode == 'val' else 'test'

    with open(os.path.join(STATISTICS_DIR, model_name, title + '.txt'), 'w+') as f:
        print('n_estimators ' + str(parameters[0]), file=f)
        print('criterion ' + str(parameters[1]), file=f)
        print('bootstrap ' + str(parameters[2]), file=f)
        print('min_samples_split ' + str(parameters[3]), file=f)
        print('min_samples_leaf ' + str(parameters[4]), file=f)
        print('max_features ' + str(parameters[5]), file=f)
        print('max_depth ' + str(parameters[6]), file=f)

        print('Training_shape ' + str(training_shape.shape), file=f)
        print(label + '_shape ' + str(validation_shape.shape), file=f)

        print('Training_accuracy ' + str(metrics_dict['acc_train']), file=f)
        print('Training_precision ' +
              str(metrics_dict['precision_train']), file=f)
        print('Training_recall ' + str(metrics_dict['recall_train']), file=f)
        print('Training_F1 ' + str(calculate_f1(
            metrics_dict['precision_train'],
            metrics_dict['recall_train'])), file=f
        )
    write_acc_prec_recall_f1(
        os.path.join(STATISTICS_DIR, model_name, title + '.txt'),
        metrics_dict,
        label,
        dict_key
    )


def write_cnn_model_statistics(title, history_dict, input_shape,
                               validation_split, parameters, model_name):
    """
    title -> string representing name of the model
    history_dict -> keras dictionary containing model statistics
    input_shape -> tuple containing training data size
    validation_split -> float describing training - validation split
    parameters -> dict containing tested parameters in and iteration
    model_name -> name of the folder where statistics will be saved 
    (defined according to ML_MODELS in settings.py)
    """
    file_path = os.path.join(STATISTICS_DIR, model_name, title + '.txt')
    with open(file_path, 'w+') as f:
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
        print(
            'Training_precision ' + str(history_dict['precision'][0]), file=f
        )
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


def plot_rf_model_statistics(title, train_score, val_score, data_name, model_name):
    '''
    title -> string representing figure title
    train_score -> Float presenting train accuracy
    val_score -> Float presenting validation accuracy
    data_name -> string describing title
    model_name -> name of the folder where statistics will be saved 
    (defined according to ML_MODELS in settings.py)
    '''
    # summarize history for accuracy
    plt.figure(title.capitalize())
    plt.bar([0, 1], [train_score, val_score])
    plt.xticks([0, 1], ('train', 'validation'))
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

    val_label = "%.4g%%" % (val_score * 100)
    plt.text(
        1,
        0.5,
        val_label,
        fontweight='bold',
        horizontalalignment='center',
        verticalalignment='center'
    )

    img_name = 'train_test_' + title.lower() + '_' + data_name + '.png'

    plt.savefig(
        os.path.join(FIGURES_DIR, model_name, img_name),
        format='png',
        dpi=300
    )
    plt.close()


def plot_cnn_model_statistics(title, train, valid, data_name, model_name):
    """
    title -> string representing figure title
    train -> list of keras values during n epoch on the training set
    valid -> list of keras values during n epoch on the validation set
    data_name -> string describing title
    model_name -> name of the folder where statistics will be saved 
    (defined according to ML_MODELS in settings.py)
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

    plt.savefig(
        os.path.join(FIGURES_DIR, model_name, img_name),
        format='png',
        dpi=300
    )
    plt.close()


def plot_confusion_matrix(cm, classes, matrix_name, model_name, normalize=False, title='', cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.

    model_name -> name of the folder where statistics will be saved 
    (defined according to ML_MODELS in settings.py)

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
        os.path.join(
            FIGURES_DIR, model_name, 'confusion_matrix_' + matrix_name + '.png'
        ),
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

    Returns tuple containing list of all amplitudes (X) and all_labels (y)
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


def get_train_data(model_name):
    """
    model_name -> string representing processed folder in which
    processed data is located.

    Returns tuple containing features and labels for train data.
    """
    file = h5py.File(os.path.join(
        PROCESSED_DATA_DIR, model_name, 'processed_data.hdf5'), 'r')

    return (
        file['x_train'].value,
        file['y_train'].value,
    )


def get_test_data(model_name):
    """
    model_name -> string representing processed folder in which
    processed data is located.

    Returns tuple containing features and labels for test data.
    """
    file = h5py.File(os.path.join(
        PROCESSED_DATA_DIR, model_name, 'processed_data.hdf5'), 'r')

    return (
        file['x_test'].value,
        file['y_test'].value,
    )


def get_folder_class_index(cut_dir_path, folder_name):
    """
    cut_dir_path -> String representing path of the cut directory.

    Returns int value of the class.
    """

    class_labels = os.listdir(cut_dir_path)
    class_labels.sort()

    try:
        return_class = class_labels.index(folder_name)
    except ValueError:
        print("Class was not found. \
            Function get_folder_class_index in data_helpers.")
        return_class = 0
    return return_class
