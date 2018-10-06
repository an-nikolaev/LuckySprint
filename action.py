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

        self.char_skills = []
        self.success_mods = []
        self.fail_mods = []

        self.get_answer_info()

        self.final_success_mods = [d + m for d, m in zip(self.get_default_mods(), self.success_mods[0])]
        self.final_fail_mods = [d + m for d, m in zip(self.get_default_mods(), self.fail_mods[0])]

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

    def get_answer_info(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        for item in actions_json[self.internal_name]["answers"]:
            if item == self.action_answer:
                self.char_skills = self.get_answer_skills()
                self.success_mods = actions_json[self.internal_name]["answers"][self.action_answer]["success"]
                self.fail_mods = actions_json[self.internal_name]["answers"][self.action_answer]["fail"]

    def get_answer_skills(self):
        with open(ACTIONS_FILE, encoding="utf-8") as jfile:
            actions_json = json.loads(jfile.read())
        answer_skills = actions_json[self.internal_name]["answers"][self.action_answer]["skills"]
        return answer_skills

