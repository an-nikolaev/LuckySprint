#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import pprint as pp
import sys
import time
from datetime import datetime

import telepot
import telepot.helper
from telepot.delegate import (
    per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from game_controller import GameController

logging.basicConfig(filename=datetime.now().strftime('logs/%Y-%m-%d_%H-%M-%S.log'), level=logging.INFO)


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
        self._sent = None
        self._editor = None

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        pp.pprint(msg)
        self._username = msg['from']['first_name']
        info(self._username, 'started new iteration: ' + msg['text'] if (content_type == 'text') else '')

        if not self._is_sprint_started:
            self._sent = self.sender.sendPhoto(
                'AgADAgAD-KkxG2TkyUluwtbim69_EOPRtw4ABJ_PE--dwgoF2YUEAAEC',
                caption='Здравствуй, путник! Решил почуствовать себя разработчиком? Ну, нажимай...',
                reply_markup=InlineKeyboardMarkup(
                    inline_keyboard=[[
                        InlineKeyboardButton(text='Начать спринт',
                                             callback_data='start'),
                    ]]
                ))

        else:
            self.sender.sendMessage('Кнопки жми давай, не понимаю рукописных ответов! 😠')

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        info(self._username, 'callback: ' + query_data)

        if query_data == 'start':
            self._is_sprint_started = True
            self._editor = telepot.helper.Editor(self.bot, self._sent)
            self._editor.deleteMessage()
            self.sender.sendMessage('*Спринт начался, погнали!* 🏎🎉👷', parse_mode='Markdown')
        else:
            self._answers[self._current_question_num] = query_data

            self._editor = telepot.helper.Editor(self.bot, self._sent)
            self._editor.editMessageText('``` Твое решение: ' + query_data + '```', parse_mode='Markdown')
            self._current_question_num += 1

        if self._current_question_num < len(self._questions):
            self._show_next_question()

        else:
            result = pp.pformat(self._gc.get_results(self._answers))
            info(self._username, 'Total result: ' + result)
            self.sender.sendMessage(
                result,
                reply_markup=None,
                parse_mode='Markdown')
            self.sender.sendMessage(
                "А теперь ты можешь попробовать найти нормальную работу на hh.ru!"
            )
            self._is_sprint_started = False
            self.close()

    def _show_next_question(self):
        question = self._questions[self._current_question_num]['question']
        choices = self._questions[self._current_question_num]['answers']
        info(self._username, 'question: ' + question + '; choices: ' + str(choices))

        self._sent = self.sender.sendMessage(
            question,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=str(c), callback_data=str(c))] for c in choices]
            )
        )


TOKEN = sys.argv[1]

telepot.api.set_proxy('https://37.252.67.184:49693')

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(types=['private']), create_open, SprintStarter, timeout=54000),
])

MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
