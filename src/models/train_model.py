import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '../..'))

from settings import TRAINING_DIR, VALIDATION_DIR, MODEL_DIR, FIGURES_DIR
import keras
import matplotlib.pyplot as plt
from model import get_model
from keras.preprocessing.image import ImageDataGenerator


# -------- required arguments --------
num_classes = int(sys.argv[1])
data_name = str(sys.argv[2])
# ------------------------------------
batch_size = 50
epochs = 12

# input image dimensions
img_rows, img_cols = 480, 20
input_shape = (img_rows, img_cols, 3)

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    featurewise_std_normalization=True,
    horizontal_flip=False
)

val_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    TRAINING_DIR + '/',
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

validation_generator = val_datagen.flow_from_directory(
    VALIDATION_DIR + '/',
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    # classes=class_labels
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

model = get_model(input_shape, num_classes)

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
    validation_steps=batch_size,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0.00001
        )
    ]
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
plt.savefig(FIGURES_DIR + '/' + 'accuracy_' + data_name + '.jpg')
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
plt.savefig(FIGURES_DIR + '/' + 'loss_' + data_name + '.jpg')

# serialize model to JSON
model_json = model.to_json()
with open(MODEL_DIR + '/' + 'model_' + data_name + '.json', 'w') as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(MODEL_DIR + '/' + 'model_' + data_name + '.h5')
print('Saved model to disk')
