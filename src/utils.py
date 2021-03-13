import os
import json

def construct_path(file) -> str:
    """Return path to file"""
    path = os.getcwd()
    path = os.path.abspath(path)
    path = os.path.dirname(path)
    path = os.path.join(path, 'data', file)
    return path


def load_json(file_name) -> dict:
    """Return read json file"""
    data = None
    path = construct_path(file_name)
    with open(path, "r", encoding='utf8') as file:
        data = json.load(file)
    return data
