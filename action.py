#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from config import ACTIONS_FILE


class Action:

    def __init__(self, external_name, action_answer):
        self.external_name = external_name
        self.action_answer = action_answer

        self.internal_name = self.get_internal_name()
        if self.internal_name == "":
            print("Action is unknown: {}".format(self.external_name))

        self.mods = self.get_default_mods()

        self.get_final_mods()

    def get_internal_name(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        for item in actions_json:
            if actions_json[item]["external_name"] == self.external_name:
                return item

    def get_default_mods(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        return actions_json[self.internal_name]["default_mods"]

    def get_final_mods(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        for item in actions_json[self.internal_name]["answers"]:
            if item == self.action_answer:
                for i in range(len(self.mods)):
                    self.mods[i] += actions_json[self.internal_name]["answers"][item][i]

    def get_action_mods(self):
        return self.mods
