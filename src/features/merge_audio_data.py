import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from helpers.file_helpers import create_directory, clear_dir
from pydub import AudioSegment
from os import listdir
from settings import RAW_DATA_DIR


def get_sopila_dirs(sopila_label):
    """
    sopila_label -> string which determines which sopila folders will
    be extracted.
    """
    sopila_dirs = []
    recordings_folders = listdir(os.path.join(RAW_DATA_DIR))
    recordings_folders.sort()
    for folder in recordings_folders:
        is_silence = 'silence' in folder
        is_merged = 'm' in folder and 'v' in folder
        if sopila_label in folder and not is_silence and not is_merged:
            sopila_dirs.append(folder)
    return sopila_dirs


def append_audio_files(folder_files, folder_name):
    # merge all mala files into one
    combined = AudioSegment.empty()
    for filename in folder_files:
        file = AudioSegment.from_wav(
            os.path.join(RAW_DATA_DIR, folder_name, filename)
        )

        combined += file
    return combined


def merge_audio_files(file1, file2, export_dirname):
    """
    file1, file2 -> must be objects of AudioSegment
    """
    # if one file is shorter than oder then just cut off at shorter length
    if file1.duration_seconds < file2.duration_seconds:
        combined = file1.overlay(file2)
    else:
        combined = file2.overlay(file1)

    # v__ is added in order to put mixed recordings after single ones
    # but before silence
    export_dir = os.path.join(RAW_DATA_DIR, 'vv_' + export_dirname)
    create_directory(export_dir)
    clear_dir(export_dir)
    combined.export(os.path.join(export_dir, export_dirname + '.wav'), format='wav')

mala_dirs = get_sopila_dirs('m')
vela_dirs = get_sopila_dirs('v')

for mala_dir in mala_dirs:

    combined_mala = append_audio_files(
        listdir(os.path.join(RAW_DATA_DIR, mala_dir)),
        mala_dir
    )

    for vela_dir in vela_dirs:

        combined_vela = append_audio_files(
            listdir(os.path.join(RAW_DATA_DIR, vela_dir)),
            vela_dir
        )
        merge_audio_files(combined_mala, combined_vela, mala_dir + vela_dir)
