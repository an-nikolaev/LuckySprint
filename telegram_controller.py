#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open


# def on_chat_message(msg):
#     content_type, chat_type, chat_id = telepot.glance(msg)
#
#     keyboard = InlineKeyboardMarkup(inline_keyboard=[
#         [InlineKeyboardButton(text='Press me', callback_data='press')],
#     ])
#
#     bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)


class GameController(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GameController, self).__init__(*args, **kwargs)
        self._count = 0

    def on_chat_message(self, msg):
        # self._count += 1
        # self.sender.sendMessage(self._count)

        content_type, chat_type, chat_id = telepot.glance(msg)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Press me', callback_data='press')],
        ])

        bot.sendMessage(chat_id, 'Use inline keyboard', reply_markup=keyboard)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print('Callback Query:', query_id, from_id, query_data)

        bot.answerCallbackQuery(query_id, text='Got it')


TOKEN = ''
telepot.api.set_proxy('https://198.58.10.139:51026')

# bot = telepot.Bot('639608498:AAEcRyoHlVRNbx3bitaJ-XBP8vfCYahT_CA')


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GameController, timeout=10),
])

MessageLoop(bot).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)
