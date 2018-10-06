#!/usr/bin/python
# -*- coding: utf-8 -*-
from action import Action
from config import NUMBER_OF_ACTIONS
from character import Character
from sprint import Sprint
from util import get_external_classes, get_external_races, get_random_actions_with_answers


class GameController:
    def __init__(self):
        self._test = 0
        self.chosen_actions = []

    def get_questions(self):
        self.chosen_actions = get_random_actions_with_answers()
        questions = \
            {
                0:
                    {
                        'question': 'Выбери свою профессию, выбирай мудро.',
                        'answers': get_external_classes()
                    },
                1:
                    {
                        'question': 'Какими дополнительными качествами ты обладаешь?',
                        'answers': get_external_races()
                    }
            }
        for i in range(2, 2 + NUMBER_OF_ACTIONS):
            questions[i] = {
                'question': next(iter(self.chosen_actions[i - 2])),
                'answers': list(self.chosen_actions[i - 2][next(iter(self.chosen_actions[i - 2]))].keys())
            }
        return questions

    def get_results(self, answers):
        answers["results"] = self.calculate_results(answers)
        return str(answers)

    def calculate_results(self, answers):
        char = Character(answers[1], answers[0])
        sprint = Sprint(char)
        actions_answers = {next(iter(self.chosen_actions[0])): answers[2], next(iter(self.chosen_actions[1])): answers[3],
                           next(iter(self.chosen_actions[2])): answers[4]}
        for action_name in actions_answers:
            action = Action(action_name, actions_answers[action_name])
            sprint.apply_action_to_sprint(action)

        results = sprint.compare_with_desired()
        return results

