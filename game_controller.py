#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import NUMBER_OF_ACTIONS
from character import Character
from sprint import Sprint
from util import get_external_classes, get_external_races, get_random_actions_with_answers


class GameController:
    def __init__(self):
        self._test = 0

    def get_questions(self):
        actions_with_answers = get_random_actions_with_answers()
        questions = \
            {
                0:
                    {
                        'question': 'Выбери расу, выбирай мудро',
                        'answers': get_external_races()
                    },
                1:
                    {
                        'question': 'Выбери класс, выбирай мудро',
                        'answers': get_external_classes()
                    }
            }
        for i in range(2, 2 + NUMBER_OF_ACTIONS):
            questions[i] = {
                'question': next(iter(actions_with_answers[i - 2])),
                'answers': list(next(iter(actions_with_answers[i - 2])))
            }
        return questions

    def get_results(self, answers):
        answers[999] = 999
        return str(answers)

    def calculate_results(self, answers):
        char = Character(answers[1], answers[0])
        sprint = Sprint()

