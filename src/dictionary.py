import json
import utils

EMPTY = '.'

DICT = None
path = utils.construct_path('phrases.json')

with open(path, "r", encoding='utf8') as file:
    DICT = json.load(file)
