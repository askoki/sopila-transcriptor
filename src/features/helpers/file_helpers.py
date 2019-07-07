import os
import errno
import shutil


def clear_dir(clear_path):
    '''
    clear_path - delete all contents of a folder
    in given path
    '''
    for root, dirs, files in os.walk(clear_path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


def create_directory(directory_path):
    '''
    directory_path - path and name of directory to be created
    '''
    try:
        os.makedirs(directory_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def create_directories(directories):
    '''
    directories - list of paths to directories
    '''
    for directory in directories:
        create_directory(directory)
