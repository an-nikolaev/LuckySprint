#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

from config import ACTIONS_FILE


class Action:

    def __init__(self, external_name, action_answers):
        self.external_name = external_name
        self.action_answers = action_answers

        self.internal_name = self.get_internal_name()
        if self.internal_name == "":
            print("Action is unknown: {}".format(self.external_name))

    def get_internal_name(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        for item in actions_json:
            if actions_json[item]["external_name"] == self.external_name:
                return item

    def get_default_mods(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())




    def apply_user_ch