#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from config import SPRINTS_FILE, DIFFICULTY, RESULT_FILE


class Sprint:

    def __init__(self, char):
        self.char = char

        # sprint optins - tasks, bugs, important_tasks, legacy, user_happiness, money

        (self.tasks, self.bugs, self.important_tasks, self.legacy,
         self.user_happiness, self.money) = self.set_random_sprint_desired_options()

        (self.fact_tasks, self.fact_bugs, self.fact_important_tasks,
         self.fact_legacy, self.fact_user_happiness, self.fact_money) = 0, 0, 0, 0, 0, 0

        self.results = {}

    @staticmethod
    def set_random_sprint_desired_options():
        with open(SPRINTS_FILE, encoding="utf-8") as jfile:
            sprints = json.loads(jfile.read())
        chosen_sprint = random.randint(0, len(sprints) - 1)
        return sprints[chosen_sprint]

    def get_result_translations(self):
        with open(RESULT_FILE, encoding="utf-8") as jfile:
            result_json = json.loads(jfile.read())
        return result_json

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
        # тут механика про то какие модификаторы брать у действия
        modificator = 0
        for i in range(4):
            modificator += random.randint(-1, 1)
        action_success = False
        for skill_index in action.char_skills:
            char_versus = self.char.skills[skill_index] + modificator
            if char_versus > DIFFICULTY:
                action_success = True
        mods = action.final_success_mods if action_success else action.final_fail_mods
        self.fact_tasks += mods[0]
        self.fact_bugs += mods[1]
        self.fact_important_tasks += mods[2]
        self.fact_legacy += mods[3]
        self.fact_user_happiness += mods[4]
        self.fact_money += mods[5]

    def compare_with_desired(self):
        # логика как считать общий результат спринта
        total_result = False
        if self.fact_tasks >= self.tasks and self.fact_important_tasks >= self.important_tasks:
            total_result = True
        if self.fact_bugs > self.bugs and self.fact_money < self.money:
            total_result = False
        if self.fact_legacy > self.legacy and self.fact_user_happiness < self.user_happiness:
            total_result = False

        result_json = self.get_result_translations()
        if self.fact_tasks < self.tasks:
            self.results["Количество выпущенных задач"] = "{}".format(result_json['tasks']['fail'])
        else:
            self.results["Количество выпущенных задач"] = "{}".format(result_json['tasks']['win'])
        if self.fact_bugs < self.bugs:
            self.results["Наплодили багов"] = "{}".format(result_json['bugs']['fail'])
        else:
            self.results["Наплодили багов"] = "{}".format(result_json['bugs']['win'])
        if self.fact_important_tasks < self.important_tasks:
            self.results["Сделано важных задач"] = "{}".format(result_json['important_tasks']['fail'])
        else:
            self.results["Сделано важных задач"] = "{}".format(result_json['important_tasks']['win'])
        if self.fact_legacy < self.legacy:
            self.results["Добавили тысяч строк легаси кода"] = "{}".format(result_json['legacy']['fail'])
        else:
            self.results["Добавили тысяч строк легаси кода"] = "{}".format(result_json['legacy']['win'])
        if self.fact_user_happiness < self.user_happiness:
            self.results["Индекс радости пользователей"] = "{}".format(result_json['user_happiness']['fail'])
        else:
            self.results["Индекс радости пользователей"] = "{}".format(result_json['user_happiness']['win'])
        if self.fact_money < self.money:
            self.results["Заработали миллионов $ для компании"] = "{}".format(result_json['money']['fail'])
        else:
            self.results["Заработали миллионов $ для компании"] = "{}".format(result_json['money']['win'])

        self.results["Общий результат"] = "Вы отлично справились! Работаем дальше" if total_result \
            else "У вас ничего не получилось. Вы уволены."
        return self.results
