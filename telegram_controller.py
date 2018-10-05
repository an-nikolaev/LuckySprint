#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import telepot.helper
import logging
from datetime import datetime
from game_controller import GameController
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

logging.basicConfig(filename=datetime.now().strftime('%Y-%m-%d_%H-%M-%S.log'), level=logging.INFO)


def info(user, s):
    return logging.info(str(datetime.now().strftime('%H:%M:%S')) + ', user: ' + user + ': ' + s)


class SprintStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(SprintStarter, self).__init__(*args, **kwargs)

        self._username = ''
        self._is_sprint_started = False
        self._gc = GameController()
        self._questions = self._gc.get_questions()
        self._current_question_num = 0
        self._answers = {}

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self._username = msg['from']['first_name']
        info(self._username, 'started new iteration')

        if not self._is_sprint_started:
            self.sender.sendMessage(
                'Нажмите, чтобы начать спринт',
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[
                        InlineKeyboardButton(text='Начать спринт', callback_data='start'),
                    ]]
                )
            )
        else:
            self.sender.sendMessage('Кнопки жми давай, не понимаю рукописных ответов')

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        info(self._username, 'callback: ' + query_data)

        if query_data == 'start':
            self._is_sprint_started = True
        else:
            self._answers[self._current_question_num] = query_data
            self._current_question_num += 1

        if self._current_question_num < len(self._questions):
            self._show_next_question()

        else:
            result = self._gc.get_results(self._answers)
            info(self._username, 'Total result: ' + result)
            self.sender.sendMessage(
                result,
                reply_markup=None)
            self._is_sprint_started = False
            self.close()

    def _show_next_question(self):
        question = self._questions[self._current_question_num]['question']
        choices = self._questions[self._current_question_num]['answers']
        info(self._username, 'question: ' + question + '; choices: ' + str(choices))

        self.sender.sendMessage(
            question,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=str(c), callback_data=str(c))] for c in choices]
            )
        )


TOKEN = sys.argv[1]

telepot.api.set_proxy('https://186.148.169.82:50797')

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(types=['private']), create_open, SprintStarter, timeout=54000),
])

MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
