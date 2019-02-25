import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..',))

from settings import MODEL_DIR, USE_GPU
import keras
import datetime
import numpy as np
from model import get_model
from features.helpers.data_helpers import plot_model_statistics, \
    get_train_data

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
data_name = str(sys.argv[2]) + '_tloss_1D_'
# ------------------------------------
batch_size = 50
epochs = 12

x_train, y_train = get_train_data()

n_rows, n_cols = x_train.shape

model = get_model((n_cols, 1), num_classes)

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy']
)

x_train = np.expand_dims(x_train, axis=3)
y_train = keras.utils.to_categorical(y_train, num_classes=num_classes, dtype='float32')

print('Before:')
print(datetime.datetime.now())
history = model.fit(
    x=x_train,
    y=y_train,
    validation_split=0.2,
    epochs=epochs,
    verbose=1,
    shuffle=True,
    steps_per_epoch=batch_size,
    validation_steps=batch_size,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss', min_delta=0.1
        )
    ]
)
print('After:')
print(datetime.datetime.now())

# list all data in history
print(history.history.keys())

# serialize model to JSON
model_json = model.to_json()
with open(os.path.join(MODEL_DIR, 'model_' + data_name + '.json'), 'w') as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(os.path.join(MODEL_DIR, 'model_' + data_name + '.h5'))
print('Saved model to disk')

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


