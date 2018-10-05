#!/usr/bin/python
# -*- coding: utf-8 -*-

from character import Character
from sprint import Sprint
from util import get_external_classes, get_external_races


class GameController:
    def __init__(self):
        self._test = 0

    def get_questions(self):
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
        return questions

    def get_results(self, answers):
        answers[999] = 999
        return str(answers)

    def calculate_results(self, answers):
        char = Character(answers[1], answers[0])
        sprint = Sprint()
