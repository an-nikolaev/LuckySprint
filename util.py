#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from config import CLASSES_FILE, RACES_FILE, NUMBER_OF_ACTIONS, ACTIONS_FILE


def get_external_classes():
    classes_list = []
    with open(CLASSES_FILE, encoding="utf-8") as jfile:
        classes_json = json.loads(jfile.read())
    for item in classes_json:
        classes_list.append(classes_json[item]["external_name"])
    return classes_list


def get_external_races():
    races_list = []
    with open(RACES_FILE, encoding="utf-8") as jfile:
        races_json = json.loads(jfile.read())
    for item in races_json:
        races_list.append(races_json[item]["external_name"])
    return races_list


def get_random_actions_with_answers():
    with open(ACTIONS_FILE, encoding="utf-8") as jfile:
        actions_json = json.loads(jfile.read())
    actions_names = random.sample(list(actions_json.keys()), 2)
    actions_and_answers = [{actions_json[name]["external_name"]: actions_json[name]["answers"]} for name in actions_names]
    return actions_and_answers