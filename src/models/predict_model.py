import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import MODEL_DIR, FIGURES_DIR, TEST_DIR, FILTER_SPECTROGRAM_DIR
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import keras
import itertools
import numpy as np


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
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

# dimensions of our images
img_height, img_width = 480, 20
input_shape = (img_height, img_width, 3)
num_classes = 12

class_labels = [
    'm0', 'm1', 'm2', 'm3', 'm4', 'm5', 'm6',
    'v0', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6'
]

# model must be the same as trained
model = Sequential()
model.add(Conv2D(
    32,
    kernel_size=(3, 3),
    activation='relu',
    input_shape=input_shape
))

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

# load the model we saved
model.load_weights(MODEL_DIR + 'model.h5')
model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy']
)

# use test set
test_datagen = image.ImageDataGenerator(rescale=1. / 255)

batch_size = 50
test_batches = test_datagen.flow_from_directory(
    TEST_DIR,
    target_size=(img_height, img_width),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical'
)


true_classes = []
predicted_classes = []

folders = os.listdir(TEST_DIR)
folders.sort()


for i, folder in enumerate(folders):

    class_folder = TEST_DIR + '/' + folder
    class_image_data = []

    for data in os.listdir(class_folder):

        image_path = class_folder + '/' + data

        img = image.load_img(image_path, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        class_image_data.append(x)

    # add true class index as many times as there are test data for that class
    true_classes.extend([i] * len(class_image_data))

    # stack arrays vertically
    array_row = np.vstack(class_image_data)

    # predicted class
    predicted_class = model.predict_classes(array_row, batch_size=20)
    predicted_classes.extend(predicted_class)


cm = confusion_matrix(true_classes, predicted_classes)
plt.figure("Confusion matrix")
plot_confusion_matrix(cm, class_labels)
plt.savefig(FIGURES_DIR + 'confusion_matrix.jpg')
plt.show()
