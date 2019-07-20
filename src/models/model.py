from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D


def get_model(input_shape, num_classes, cnn_layers=1, num_filters=16, filter_size=3, hidden_layers=64):
    """
    return keras model (used in training and prediction)
    input_shape -> tuple containing targeted size (rows, cols)
    num_classes -> integer containing number of classes
    """
    model = Sequential()
    # cnn_layers 1, num_filters 64, filter size 3, hidden layers 64 pada
    if num_filters >= 64:
        first_layer = 32
    else:
        first_layer = num_filters
    
    
    model.add(Conv1D(
        first_layer,
        kernel_size=filter_size,
        activation='relu',
        input_shape=input_shape
    ))
   
    model.add(MaxPooling1D(2))
    for layers in range(cnn_layers - 1):
        model.add(Conv1D(num_filters, filter_size, activation='relu'))
        model.add(MaxPooling1D(2))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(hidden_layers, activation='relu'))
    model.add(Dropout(0.5))
    # softmax predicts 1 of many classes
    # sigmoid is used both binary and multi-label classification problems,
    # where multiple classes might be 1 in the output
    model.add(Dense(num_classes, activation='softmax'))

    return model
