import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import TRAINING_DIR, VALIDATION_DIR, MODEL_DIR, FIGURES_DIR
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.preprocessing.image import ImageDataGenerator

batch_size = 50
epochs = 12

# input image dimensions
img_rows, img_cols = 480, 20
input_shape = (img_rows, img_cols, 3)
num_classes = 12

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    featurewise_std_normalization=True,
    horizontal_flip=False
)

val_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    TRAINING_DIR,
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

validation_generator = val_datagen.flow_from_directory(
    VALIDATION_DIR,
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    # classes=class_labels
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

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

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy']
)

history = model.fit_generator(
    train_generator,
    steps_per_epoch=batch_size,
    epochs=epochs,
    verbose=1,
    validation_data=validation_generator,
    validation_steps=batch_size
)

# list all data in history
print(history.history.keys())

# summarize history for accuracy
plt.figure('Accuracy')
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
# plt.show()
plt.savefig(FIGURES_DIR + 'accuracy.jpg')
plt.clf()

# summarize history for loss
plt.figure('Loss')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
# plt.show()
plt.savefig(FIGURES_DIR + 'loss.jpg')

# serialize model to JSON
model_json = model.to_json()
with open(MODEL_DIR + 'model.json', 'w') as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(MODEL_DIR + 'model.h5')
print('Saved model to disk')
