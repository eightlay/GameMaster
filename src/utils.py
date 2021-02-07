import os


def construct_path(file) -> str:
    """Return path to file"""
    path = os.getcwd()
    path = os.path.abspath(path)
    path = os.path.dirname(path)
    path = os.path.join(path, 'data', file)
    return path