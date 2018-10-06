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
        self.current_answer_num = 0
        self.chosen_actions = []
        self.actions_answers = {}
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

    def get_results(self, answers):
        answers["results"] = self.calculate_results()
        return answers

    def create_character(self, character_answers):
        char = Character(character_answers[0], character_answers[1])
        self.sprint = Sprint(char)

    def set_answer(self, answer):
        self.actions_answers[next(iter(answer))] = answer[next(iter(answer))]
        self.current_answer_num += 1

    def calculate_results(self):
        # TODO: адаптировать код под количество вопросов в настройках

        for action_name in self.actions_answers:
            action = Action(action_name, self.actions_answers[action_name])
            self.sprint.apply_action_to_sprint(action)

        results = self.sprint.compare_with_desired()
        return results
