#!/usr/bin/python
# -*- coding: utf-8 -*-
from action import Action
from character import Character
from config import NUMBER_OF_ACTIONS
from sprint import Sprint
from util import get_external_classes, get_external_races, get_random_actions_with_answers


def get_character_questions():
    character_questions = \
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

    return character_questions


class GameController:
    def __init__(self):
        self._test = 0
        self.chosen_actions = []
        self.sprint = None

    def get_questions(self):
        self.chosen_actions = get_random_actions_with_answers()
        questions = {}
        for i in range(0, NUMBER_OF_ACTIONS):
            questions[i] = {
                'question': next(iter(self.chosen_actions[i - 2])),
                'answers': list(self.chosen_actions[i - 2][next(iter(self.chosen_actions[i - 2]))].keys())
            }
        return questions

    def get_results(self):
        msg, total_result = self.calculate_results()
        return msg, total_result

    def create_character(self, character_answers):
        char = Character(character_answers[0], character_answers[1])
        self.sprint = Sprint(char)

    def set_answer(self, answer):
        action = Action(next(iter(answer)), answer[next(iter(answer))])

        return self.sprint.apply_action_to_sprint(action)

    def calculate_results(self):
        results, total_result = self.sprint.compare_with_desired()
        return results, total_result
