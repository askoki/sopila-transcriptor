import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..',))

from settings import TRAINING_DIR, VALIDATION_DIR, MODEL_DIR, USE_GPU
import keras
from model import get_model
from features.helpers.data_helpers import plot_model_statistics
from keras.preprocessing.image import ImageDataGenerator

if USE_GPU:
    # use if you are running on a PC with many GPU-s
    # needs to be at the beginning of the file
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # the GPU id to use, usually either "0" or "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "1"
    # just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

# -------- required arguments --------
num_classes = int(sys.argv[1])
data_name = str(sys.argv[2]) + '_tloss'
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
    os.path.join(TRAINING_DIR),
    target_size=(img_rows, img_cols),
    color_mode='rgb',
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

validation_generator = val_datagen.flow_from_directory(
    os.path.join(VALIDATION_DIR),
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
            monitor='train_loss', min_delta=0.00001
        )
    ]
)

# list all data in history
print(history.history.keys())

# summarize history for accuracy
plot_model_statistics(
    'accuracy',
    history.history['acc'],
    history.history['val_acc'],
    data_name
)

# summarize history for loss
plot_model_statistics(
    'loss',
    history.history['loss'],
    history.history['val_loss'],
    data_name
)

# serialize model to JSON
model_json = model.to_json()
with open(os.path.join(MODEL_DIR, 'model_' + data_name + '.json'), 'w') as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(os.path.join(MODEL_DIR, 'model_' + data_name + '.h5'))
print('Saved model to disk')
