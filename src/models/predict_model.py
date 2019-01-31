import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import MODEL_DIR, TEST_DIR, FILTER_SPECTROGRAM_DIR

from model import get_model
from features.helpers.file_helpers import save_list_to_file
from features.helpers.file_helpers import save_list_to_file

import matplotlib.pyplot as plt
from keras.preprocessing import image
import keras
import numpy as np

# number of classes required argument
num_classes = int(sys.argv[1])

# provide model name
model_name = str(sys.argv[2]) + '_tloss'
matrix_name = sys.argv[3] + '_tloss'

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
plot_confusion_matrix(cm, class_labels)

# ------ real data predict

from settings import REAL_DATA_FILTER_SPEC, REAL_DATA_FILES_DIR

filepath = os.path.join(REAL_DATA_FILES_DIR, model_name + '.txt')

# create new file with same name
file = open(filepath, 'w')
file.close()

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
        image_path = os.path.join(class_folder, data)

        img = image.load_img(image_path, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        class_image_data.append(x)

    # stack arrays vertically
    array_row = np.vstack(class_image_data)

    # predicted class
    predicted_class = model.predict_classes(array_row, batch_size=20)
    save_list_to_file(filepath, predicted_class, folder)
