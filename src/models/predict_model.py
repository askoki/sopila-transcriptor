import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import MODEL_DIR, CUT_DIR
from keras.preprocessing import image
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
import keras
import numpy as np

# dimensions of our images
img_width, img_height = 480, 20
input_shape = (img_width, img_height, 3)
num_classes = 12

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

# predicting images
images = [
    CUT_DIR + 'm0/15.png',
    CUT_DIR + 'm1/15.png',
    CUT_DIR + 'm2/15.png',
    CUT_DIR + 'm3/15.png',
    CUT_DIR + 'm4/15.png',
    CUT_DIR + 'm5/15.png',
    CUT_DIR + 'v0/15.png',
    CUT_DIR + 'v1/15.png',
    CUT_DIR + 'v2/15.png',
    CUT_DIR + 'v3/15.png',
    CUT_DIR + 'v4/15.png',
    CUT_DIR + 'v5/15.png',
    CUT_DIR + 'm0/15.png',
    CUT_DIR + 'm1/4.png',
    CUT_DIR + 'm2/5.png',
    CUT_DIR + 'm3/5.png',
    CUT_DIR + 'm4/5.png',
    CUT_DIR + 'm5/5.png',
    CUT_DIR + 'v0/5.png',
    CUT_DIR + 'v1/5.png',
    CUT_DIR + 'v2/5.png',
    CUT_DIR + 'v3/5.png',
    CUT_DIR + 'v4/5.png',
    CUT_DIR + 'v5/5.png',
]

image_data = []
for image_path in images:
    img = image.load_img(image_path, target_size=(img_width, img_height))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    image_data.append(x)

# pass the list of multiple images np.vstack()
images = np.vstack(image_data)
classes = model.predict_classes(images, batch_size=12)

# print the classes, the images belong to
print(classes)