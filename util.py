import json

from config import CLASSES_FILE, RACES_FILE


def get_external_classes():
    classes_list = []
    with open(CLASSES_FILE) as jfile:
        classes_json = json.loads(jfile.read())
    for item in classes_json:
        classes_list.append(classes_json[item]["external_name"])
    return classes_list


def get_external_races():
    races_list = []
    with open(RACES_FILE) as jfile:
        races_json = json.loads(jfile.read())
    for item in races_json:
        races_list.append(races_json[item]["external_name"])
    return races_list