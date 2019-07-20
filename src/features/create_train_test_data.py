import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from settings import PROCESSED_DATA_DIR
from features.helpers.data_helpers import get_data
from sklearn.model_selection import train_test_split
import h5py


if not sys.argv[1]:
    print('Enter path of processed data dir')
    sys.exit()

DATA_PATH = os.path.join(str(sys.argv[1]))


if not sys.argv[2]:
    print('Enter boolean if data is unfiltered (True) or filtered using DFT (False)')
    sys.exit()

is_unfiltered = (sys.argv[2] == 'True')

if not sys.argv[3]:
    print('Enter boolean is model random forest or CNN')
    sys.exit()

is_random_forest = (sys.argv[3] == 'True')

if not sys.argv[4]:
    print('Enter model name defined in settings.py')
    sys.exit()

model = str(sys.argv[4])

X, y = get_data(DATA_PATH, is_unfiltered)
x_train, x_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

processed_data_file = h5py.File(
    os.path.join(PROCESSED_DATA_DIR, model, 'processed_data.hdf5'),
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

dt = 'i'
if is_random_forest:
    # PY3 unicode
    y_train = [y.encode('utf8') for y in y_train]
    y_test = [y.encode('utf8') for y in y_test]
    dt = h5py.special_dtype(vlen=str)

processed_data_file.create_dataset(
    'y_train',
    data=y_train,
    dtype=dt
)

processed_data_file.create_dataset(
    'y_test',
    data=y_test,
    dtype=dt
)
