#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from config import SPRINTS_FILE


class Sprint:

    def __init__(self, char):
        self.char = char

        # sprint optins - tasks, bugs, important_tasks, legacy, user_happiness, money

        (self.tasks, self.bugs, self.important_tasks, self.legacy,
         self.user_happiness, self.money) = self.set_random_sprint_desired_options()

        (self.fact_tasks, self.fact_bugs, self.fact_important_tasks,
         self.fact_legacy, self.fact_user_happiness, self.fact_money) = 0, 0, 0, 0, 0, 0

    @staticmethod
    def set_random_sprint_desired_options():
        with open(SPRINTS_FILE, encoding="utf-8") as jfile:
            sprints = json.loads(jfile.read())
        chosen_sprint = random.randint(1, len(sprints))
        return sprints[chosen_sprint]

    def get_sprint_description(self):
        description = {
            "tasks": self.tasks,
            "bugs": self.bugs,
            "important tasks": self.important_tasks,
            "legacy": self.legacy,
            "user happiness": self.user_happiness,
            "money": self.money

        }
        return description

    def apply_action_to_sprint(self, action):
        modificator = 4 * random.randint(-1, 1)
        mods = []
        self.fact_tasks += action.mods[0]
        self.fact_bugs += action.mods[1]
        self.fact_important_tasks += action.mods[2]
        self.fact_legacy += action.mods[3]
        self.fact_user_happiness += action.mods[4]
        self.fact_money += action.mods[5]

    def compare_with_desired(self):
        pass
