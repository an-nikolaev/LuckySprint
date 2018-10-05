#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random

from config import SPRINTS_FILE, DIFFICULTY


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

        self.results["Общий результат"] = "Вы отлично справились!" if total_result else "У вас ничего не получилось. Вы уволены."
        self.results["Количество выпущенных задач"] = "Фактически: {}, Ожидалось: {}".format(self.fact_tasks, self.tasks)
        self.results["Наплодили багов"] = "Фактически: {}, Ожидалось: {}".format(self.fact_bugs, self.bugs)
        self.results["Сделано важных задач"] = "Фактически: {}, Ожидалось: {}".format(self.fact_important_tasks, self.important_tasks)
        self.results["Добавили тысяч строк легаси кода"] = "Фактически: {}, Ожидалось: {}".format(self.fact_legacy, self.legacy)
        self.results["Индекс радости пользователей"] = "Фактически: {}, Ожидалось: {}".format(self.fact_user_happiness, self.user_happiness)
        self.results["Заработали миллионов $ для компании"] = "Фактически: {}, Ожидалось: {}".format(self.fact_money, self.money)
        return self.results
