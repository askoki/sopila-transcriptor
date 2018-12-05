import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(ROOT_DIR, 'data/')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw/')
INTERIM_DATA_DIR = os.path.join(DATA_DIR, 'interim/')
PROCESSED_DATA_DIR  = os.path.join(DATA_DIR, 'processed/')

SPECTROGRAM_PATH = os.path.join(INTERIM_DATA_DIR, 'spectrograms/')
FILTER_DIR = os.path.join(INTERIM_DATA_DIR, 'filter/')
FILTER_SPECTROGRAM_DIR = os.path.join(INTERIM_DATA_DIR, 'filter+spectrograms/')
CUT_DIR = os.path.join(INTERIM_DATA_DIR, 'cut_recordings/')

TRAINING_DIR = os.path.join(PROCESSED_DATA_DIR, 'training/')
VALIDATION_DIR = os.path.join(PROCESSED_DATA_DIR, 'validation/')
TEST_DIR = os.path.join(PROCESSED_DATA_DIR, 'test/')

MODEL_DIR = os.path.join(ROOT_DIR, 'models/')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports/')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures/')

# test
REAL_DATA_DIR = os.path.join(DATA_DIR, 'real_data/')

REAL_DATA_CUT = os.path.join(REAL_DATA_DIR, 'cut/')
REAL_DATA_RAW = os.path.join(REAL_DATA_DIR, 'raw/')
REAL_DATA_SPEC = os.path.join(REAL_DATA_DIR, 'spec/')
REAL_DATA_FILTER_SPEC = os.path.join(REAL_DATA_DIR, 'spec+filter/')
