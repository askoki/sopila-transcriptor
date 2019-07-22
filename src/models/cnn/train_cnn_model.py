import os
import sys
import datetime
import numpy as np
import keras
from keras_metrics import precision, recall
sys.path.insert(1, os.path.join(sys.path[0], '..', '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from settings import MODEL_DIR, USE_GPU
from model import get_model
from features.helpers.data_helpers import plot_cnn_model_statistics, \
    get_train_data, write_cnn_model_statistics, string_to_list

if USE_GPU:
    from keras.utils import multi_gpu_model
    # use if you are running on a PC with many GPU-s
    # needs to be at the beginning of the file
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    # the GPU id to use, usually either "0" or "1"
    os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2"
    # just disables the warning, doesn't enable AVX/FMA
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"


# -------- required arguments --------

if not sys.argv[1]:
    print('Enter model name defined in settings.py')
    sys.exit()

ML_MODEL = str(sys.argv[1])

if not sys.argv[2]:
    print(
        'Enter training parameters in the following order: cnn_layers, \
        num_filters, filter_size, hidden_layers'
    )
    sys.exit()


parameters = string_to_list(sys.argv[2])

if not sys.argv[3]:
    print('Pass True as an argument if you would like to save a model.')
    sys.exit()

save_model = (sys.argv[3] == 'True')

if not sys.argv[4]:
    print('Enter number of classes to be trained.')
    sys.exit()

num_classes = int(sys.argv[4])

# ---------------- END OF ARGUMENTS --------------------

batch_size = 1000
epochs = 12

x_train, y_train = get_train_data(ML_MODEL)
n_rows, n_cols = x_train.shape

x_train = np.expand_dims(x_train, axis=3)
y_train = keras.utils.to_categorical(
    y_train, num_classes=num_classes
)

validation_split = 0.2

print(
    'Parameters cnn_layers %s, num_filters %s, filter size %s, hidden layers %s' %
    (parameters[0], parameters[1], parameters[2], parameters[3])
)

model = get_model(
    (n_cols, 1),
    num_classes,
    cnn_layers=parameters[0],
    num_filters=parameters[1],
    filter_size=parameters[2],
    hidden_layers=parameters[3]
)

if USE_GPU:
    model = multi_gpu_model(model, gpus=[0, 1, 2])

model.compile(
    loss=keras.losses.categorical_crossentropy,
    optimizer=keras.optimizers.Adadelta(),
    metrics=['accuracy', precision(), recall()]
)

print('Before:')
print(datetime.datetime.now())
history = model.fit(
    x=x_train,
    y=y_train,
    validation_split=validation_split,
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

name = ML_MODEL
for i in range(len(parameters)):
    name += '_' + str(parameters[i])


model_path = os.path.join(MODEL_DIR, ML_MODEL, 'model_' + name)
with open(model_path + '.json','w') as json_file:
    json_file.write(model_json)

# serialize weights to HDF5
model.save_weights(model_path + '.h5')
print('Saved model to disk')

write_cnn_model_statistics(
    name,
    history.history,
    x_train.shape,
    validation_split,
    parameters,
    ML_MODEL
)

# summarize history for accuracy
plot_cnn_model_statistics(
    'accuracy',
    history.history['acc'],
    history.history['val_acc'],
    name,
    ML_MODEL
)

# summarize history for loss
plot_cnn_model_statistics(
    'loss',
    history.history['loss'],
    history.history['val_loss'],
    name,
    ML_MODEL
)
