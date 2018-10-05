#!/usr/bin/python
# -*- coding: utf-8 -*-


class GameController:
    def __init__(self):
        self._test = 0

    def get_questions(self):
        questions = \
            {
                0:
                    {
                        'question': 'Выбери расу, выбирай мудро',
                        'answers': [('Go-Go-ерша', 0), ('Мудро', 1), ('Олег', 2)]
                    }
            }
        return questions

    def get_results(self, answers):
        answers[999] = 999
        return str(answers)
