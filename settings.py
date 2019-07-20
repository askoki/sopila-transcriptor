import os
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(ROOT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
INTERIM_DATA_DIR = os.path.join(DATA_DIR, 'interim')
UNFILTERED_PATH = os.path.join(INTERIM_DATA_DIR, 'unfiltered_recordings')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

AMPLITUDE_ARRAY_PATH = os.path.join(INTERIM_DATA_DIR, 'amplitude_array')
CUT_DIR = os.path.join(INTERIM_DATA_DIR, 'cut_recordings')

TRAINING_DIR = os.path.join(PROCESSED_DATA_DIR, 'training')
VALIDATION_DIR = os.path.join(PROCESSED_DATA_DIR, 'validation')
TEST_DIR = os.path.join(PROCESSED_DATA_DIR, 'test')

MODEL_DIR = os.path.join(ROOT_DIR, 'models')
REPORTS_DIR = os.path.join(ROOT_DIR, 'reports')
FIGURES_DIR = os.path.join(REPORTS_DIR, 'figures')
STATISTICS_DIR = os.path.join(REPORTS_DIR, 'statistics')

# test
REAL_DATA_DIR = os.path.join(DATA_DIR, 'real_data')
REAL_DATA_CUT = os.path.join(REAL_DATA_DIR, 'cut')
REAL_DATA_RAW = os.path.join(REAL_DATA_DIR, 'raw')
REAL_DATA_AMP = os.path.join(REAL_DATA_DIR, 'amp')
REAL_DATA_PREDICTIONS = os.path.join(REAL_DATA_DIR, 'predictions')

SHEETS_DIR = os.path.join(REPORTS_DIR, 'sheets')

ML_MODELS = [
    {
        'name': 'mono_rf',
        'model_type': 'rf',
        'voice_type': 'mono',
        'unfiltered': True
    },
    {
        'name': 'mono_rf_dft',
        'model_type': 'rf',
        'voice_type': 'mono',
        'unfiltered': False
    },
    {
        'name': 'mono_cnn',
        'model_type': 'cnn',
        'voice_type': 'mono',
        'unfiltered': True
    },
    {
        'name': 'mono_cnn_dft',
        'model_type': 'cnn',
        'voice_type': 'mono',
        'unfiltered': False
    },
    {
        'name': 'poly_rf',
        'model_type': 'rf',
        'voice_type': 'poly',
        'unfiltered': True
    },
    {
        'name': 'poly_rf_dft',
        'model_type': 'rf',
        'voice_type': 'poly',
        'unfiltered': False
    },
    {
        'name': 'poly_cnn',
        'model_type': 'cnn',
        'voice_type': 'poly',
        'unfiltered': True
    },
    {
        'name': 'poly_cnn_dft',
        'model_type': 'cnn',
        'voice_type': 'poly',
        'unfiltered': False
    },
]

with open(os.path.join(ROOT_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        err = "Set the %s in secrets.json file." % setting
        print(err)


NUMBER_OF_CORES = get_secret("NUMBER_OF_CORES")
USE_GPU = get_secret("USE_GPU")

#  ---------------- sheet_generator settings ----------------
ABJAD_TONES = {
    # mala tones
    'm5': "gss'",
    'm4': "as'",
    'm3': "b'",
    'm2': "c''",
    'm1': "d''",
    'm0': "ef''",
    # vela tones
    'v5': "b",
    'v4': "c'",
    'v3': "d'",
    'v2': "ef'",
    'v1': "f'",
    'v0': "gf'",
    'pause': "r"  # pause
}

BEATS_PER_MINUTE = 60
BEATS_PER_SECOND = BEATS_PER_MINUTE / 60

# time frame length in s
TIMEFRAME_LENGTH = 0.04
BEAT = BEATS_PER_SECOND / TIMEFRAME_LENGTH
