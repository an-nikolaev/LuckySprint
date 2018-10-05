#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import telepot.helper
from game_controller import GameController
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

"""
$ python3.5 quiz.py <token>

Send a chat message to the bot. It will give you a math quiz. Stay silent for
10 seconds to end the quiz.

It handles callback query by their origins. All callback query originated from
the same chat message will be handled by the same `CallbackQueryOriginHandler`.
"""


class SprintStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(SprintStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage(
            'Нажмите, чтобы начать спринт',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='Начать спринт', callback_data='start'),
                ]]
            )
        )
        self.close()  # let Quizzer take over


class Quizzer(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Quizzer, self).__init__(*args, **kwargs)
        self.gc = GameController()

        self._questions = self.gc.get_questions()
        self._current_question_num = 0
        self._answers = {}

    def _show_next_question(self):

        question = self._questions[self._current_question_num]['question']
        choices = self._questions[self._current_question_num]['answers']

        self.editor.editMessageText(question,
                                    reply_markup=InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            list(map(lambda c: InlineKeyboardButton(text=str(c[0]), callback_data=c[1]),
                                                     choices))
                                        ]
                                    )
                                    )
        # return answer

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data != 'start':
            self._answers[self._current_question_num] = query_data

        if self._current_question_num < len(self._questions):
            self._show_next_question()
            self._current_question_num += 1
        else:
            self.editor.editMessageText(
                self.gc.get_results(self._answers),
                reply_markup=None)
            self.close()


TOKEN = sys.argv[1]

telepot.api.set_proxy('https://190.152.14.122:32356')

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, SprintStarter, timeout=3),
    pave_event_space()(
        per_callback_query_origin(), create_open, Quizzer, timeout=54000),
])

MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
