from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D


def get_model(input_shape, num_classes):
    '''
    return keras model (used in training and prediction)
    input_shape -> tuple containing targeted size (rows, cols)
    num_classes -> integer containing number of classes
    '''
    model = Sequential()
    model.add(Conv1D(
        32,
        kernel_size=10,
        activation='relu',
        input_shape=input_shape
    ))

    model.add(Conv1D(64, 10, activation='relu'))
    model.add(MaxPooling1D(3))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    # softmax predicts 1 of many classes
    # sigmoid is used both binary and multi-label classification problems,
    # where multiple classes might be 1 in the output
    model.add(Dense(num_classes, activation='softmax'))

    return model
