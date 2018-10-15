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

from data.images_ids import get_img_dict
from game_controller import GameController, get_character_questions

logging.basicConfig(filename=datetime.now().strftime('logs/%Y-%m-%d.log'), level=logging.INFO)
logger = logging.getLogger('lucky_bot')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

imgs = get_img_dict()


def info(user, s):
    return logger.info('user: ' + user + ': ' + s)


class SprintStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(SprintStarter, self).__init__(*args, **kwargs)

        self._username = ''
        self._is_character_created = False
        self._is_sprint_started = False
        self._gc = GameController()
        self._character_questions = get_character_questions()
        self._questions = self._gc.get_questions()
        self._current_question_num = 0
        self._character_answers = {}
        self._sent = None
        self._editor = None
        self.question = None

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        pp.pprint(msg)
        self._username = msg['from']['first_name']
        info(self._username, 'started new iteration: ' + msg['text'] if (content_type == 'text') else '')

        if not self._is_sprint_started:
            self._sent = self.sender.sendPhoto(
                imgs['welcome'],
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
            self.sender.sendMessage('*Спринт начался, погнали!* 🏎🛠👷', parse_mode='Markdown')
        else:
            if not self._is_character_created:
                self._character_answers[self._current_question_num] = query_data
                self._current_question_num += 1

                self._editor = telepot.helper.Editor(self.bot, self._sent)
                self._editor.editMessageText('``` Твое решение: ' + query_data + '```', parse_mode='Markdown')
                if self._current_question_num == 2:
                    self._is_character_created = True
                    self._current_question_num = 0
                    self._gc.create_character(self._character_answers)

            else:
                result_msg = self._gc.set_answer({self.question: query_data})

                self._editor = telepot.helper.Editor(self.bot, self._sent)
                self._editor.editMessageText('*Проблема*:\n%s\n\n*Твое решение*:\n%s\n\n*Результат*:\n%s' %
                                             (self._questions[self._current_question_num]['question'], query_data,
                                              result_msg), parse_mode='Markdown')

                self._current_question_num += 1

        if self._current_question_num < len(self._questions):
            self._show_next_question()

        else:
            result, is_win = self._gc.get_results()
            info(self._username, 'Total result: ' + str(result))
            if is_win:
                self._sent = self.sender.sendPhoto(
                    imgs['success'],
                    caption='🎉')
            else:
                self._sent = self.sender.sendPhoto(
                    imgs['fail'],
                    caption='😕')

            self.sender.sendMessage(
                str(result),
                reply_markup=None,
                parse_mode='Markdown')
            self.sender.sendMessage(
                "А теперь ты можешь попробовать найти *нормальную* работу на hh.ru!",
                parse_mode='Markdown'
            )
            self._is_sprint_started = False
            self.close()

    def _show_next_question(self):
        self.question = self._questions[self._current_question_num]['question'] if self._is_character_created else \
            self._character_questions[self._current_question_num]['question']
        choices = self._questions[self._current_question_num]['answers'] if self._is_character_created else \
            self._character_questions[self._current_question_num]['answers']
        info(self._username, 'question: ' + self.question + '; choices: ' + str(choices))

        self._sent = self.sender.sendMessage(
            self.question,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=str(c), callback_data=str(c))] for c in choices]
            )
        )


TOKEN = sys.argv[1]
PROXY = sys.argv[2]

# https://89.165.218.82:47886
telepot.api.set_proxy(PROXY)

bot = telepot.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
        per_chat_id(types=['private']), create_open, SprintStarter, timeout=54000),
])

MessageLoop(bot).run_as_thread()
info('Bot', 'Listening ...')

while 1:
    time.sleep(10)
