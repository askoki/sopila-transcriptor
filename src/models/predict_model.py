import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import MODEL_DIR, FIGURES_DIR, TEST_DIR, FILTER_SPECTROGRAM_DIR
from keras.preprocessing import image
from sklearn.metrics import confusion_matrix
from model import get_model
import matplotlib.pyplot as plt
import keras
import itertools
import re
import numpy as np

# number of classes required argument
num_classes = int(sys.argv[1])

# provide model name
model_name = str(sys.argv[2]) + '_tloss'
matrix_name = sys.argv[3] + '_tloss'


def natural_sort(l):
    '''
    needed in order to sort numbers and strings
    '''
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

# took from scikit-learn.org example


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

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


def save_list_to_file(file, predicted_list, filename):
    file.write('\n#' + filename + '\n')
    list_to_string = '['
    for line in predicted_list:
        list_to_string += str(line) + ' '
    list_to_string = list_to_string[:-1] + ']'
    file.write(list_to_string)

# dimensions of our images
img_height, img_width = 480, 20
input_shape = (img_height, img_width, 3)

# use test set
test_datagen = image.ImageDataGenerator(rescale=1. / 255)
batch_size = 50


class_labels = [
    'm0', 'm1', 'm2', 'm3', 'm4', 'm5',
    'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'blank',
]

# model must be the same as trained
model = get_model(input_shape, num_classes)

# load the model we saved
model.load_weights(os.path.join(MODEL_DIR, model_name + '.h5'))
model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy']
)

test_batches = test_datagen.flow_from_directory(
    os.path.join(TEST_DIR),
    target_size=(img_height, img_width),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical'
)

true_classes = []
predicted_classes = []

folders = os.listdir(os.path.join(TEST_DIR))
folders = natural_sort(folders)

for i, folder in enumerate(folders):

    class_folder = os.path.join(TEST_DIR, folder)
    class_image_data = []

    for data in os.listdir(class_folder):

        image_path = os.path.join(class_folder, data)

        img = image.load_img(
            image_path, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        class_image_data.append(x)

    # add true class index as many times as there are test data for that
    # class
    true_classes.extend([i] * len(class_image_data))

    # stack arrays vertically
    array_row = np.vstack(class_image_data)

    # predicted class
    predicted_class = model.predict_classes(array_row, batch_size=20)
    predicted_classes.extend(predicted_class)

cm = confusion_matrix(true_classes, predicted_classes)
plt.figure("Confusion matrix")
plot_confusion_matrix(cm, class_labels)
plt.savefig(
    os.path.join(FIGURES_DIR, 'confusion_matrix_' + matrix_name + '.jpg')
)
plt.clf()
plt.clf()
plt.close()

# ------ real data predict

from settings import REAL_DATA_FILTER_SPEC, REAL_DATA_FILES_DIR

# create new file with same name
file = open(os.path.join(REAL_DATA_FILES_DIR, model_name + '.txt'), 'w')
file.close()
# open file in append mode
file = open(os.path.join(REAL_DATA_FILES_DIR, model_name + '.txt'), 'a+')

test_batches = test_datagen.flow_from_directory(
    REAL_DATA_FILTER_SPEC,
    target_size=(img_height, img_width),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical'
)

true_classes = []
predicted_classes = []

folders = os.listdir(os.path.join(REAL_DATA_FILTER_SPEC))
folders.sort()

for i, folder in enumerate(folders):

    class_folder = os.path.join(REAL_DATA_FILTER_SPEC, folder)
    class_image_data = []

    files_sorted = os.listdir(class_folder)
    files_sorted = natural_sort(files_sorted)
    for data in files_sorted:

        image_path = class_folder + '/' + data

        img = image.load_img(
            image_path, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        class_image_data.append(x)

    # stack arrays vertically
    array_row = np.vstack(class_image_data)

    # predicted class
    predicted_class = model.predict_classes(array_row, batch_size=20)
    save_list_to_file(file, predicted_class, folder)
file.close()
