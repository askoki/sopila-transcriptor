import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import PROCESSED_DATA_DIR, UNFILTERED_PATH
from features.helpers.data_helpers import get_random_forest_data
from sklearn.model_selection import train_test_split
import h5py

# X, y = get_random_forest_data(UNFILTERED_PATH)
X, y = get_random_forest_data()
x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42)

processed_data_file = h5py.File(
    os.path.join(PROCESSED_DATA_DIR, 'processed_data.hdf5'),
    'w'
)

processed_data_file.create_dataset(
    'x_train',
    data=x_train,
    dtype='f'
)

processed_data_file.create_dataset(
    'x_test',
    data=x_test,
    dtype='f'
)

# PY3 unicode
y_train = [y.encode('utf8') for y in y_train]
dt = h5py.special_dtype(vlen=str)

processed_data_file.create_dataset(
    'y_train',
    data=y_train,
    dtype=dt
)

y_test = [y.encode('utf8') for y in y_test]
processed_data_file.create_dataset(
    'y_test',
    data=y_test,
    dtype=dt
)
