#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.
#
# THIS EXAMPLE HAS BEEN UPDATED TO WORK WITH THE BETA VERSION 12 OF PYTHON-TELEGRAM-BOT.
# If you're still using version 11.1.0, please see the examples at
# https://github.com/python-telegram-bot/python-telegram-bot/tree/v11.1.0/examples

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, ConversationHandler, MessageHandler, Filters)

token = os.environ.get('BOT_TOKEN', '5124929855:AAGHPfPqP8e1K-h7oX2cpD7R1XAhPDrlVsk')

# Enable logging

game_description, rules, question, answer, one_more, good_bye = range(6)


def start(update, context):
    reply_keyboard = [['OK']]

    update.message.reply_text(
        "Привет, эта игра будет угадывать число, которое ты загадал | нажми любую кнопку что-бы продолжить",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return game_description


def game_description(update, context):
    reply_keyboard = [['OK']]

    update.message.reply_text(
        "И так, загадай любое целое число от 1 до 100, а я попробую его отгадать| нажми любую кнопку что-бы продолжить",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return rules


def rules(update, context):
    context.chat_data['rng'] = list(range(1, 101))
    reply_keyboard = [['Да понял я уже, давай играть!']]

    update.message.reply_text(
        "Я буду задавать вопросы, а ты говори, число меньше или больше. | ну что, начнем? только не жульничай :)",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return question


def collecting_stats():
    pass


def question(update, context):
    reply_keyboard = [['меньше'], ['больше/равно']]
    reply_keyboard_2 = [['правильно'],['неправильно']]
    text = update.message.text

    if len(context.chat_data['rng']) == 1:
        update.message.reply_text(
            f"Твое число {context.chat_data['rng']} это было ваще изи.",reply_markup=ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=True))
        context.chat_data['rng'] = list(range(1, 100 + 1))
        return one_more
    if text == 'больше/равно':
        del context.chat_data['rng'][:int((len(context.chat_data['rng'])) / 2)]

        update.message.reply_text(
            f"Твое число больше или меньше {context.chat_data['rng'][int(len(context.chat_data['rng']) / 2)]}",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))
    elif text == 'меньше':
        del context.chat_data['rng'][int((len(context.chat_data['rng'])) / 2):]

        update.message.reply_text(
            f"Твое число больше или меньше {context.chat_data['rng'][int(len(context.chat_data['rng']) / 2)]}",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))
    else:
        update.message.reply_text(
            f"Твое число больше или меньше {context.chat_data['rng'][int(len(context.chat_data['rng']) / 2)]}",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False))

    return question


def one_more(update, context):
    reply_keyboard = [['да'], ['нет']]
    update.message.reply_text('Хочешь сыграть еще ?',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return one_more


def good_bye(update, context):
    collecting_stats()
    update.message.reply_text("Приятно было с тобой поиграть :) до встречи в следующей игре 👋👋👋")
    # update.message.reply_text(f"Кстати, ciekawostka od Mariana, всего было сиграно {15} игр")

    return ConversationHandler.END


def cancel(update, context):
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            game_description: [MessageHandler(Filters.text, game_description)],

            rules: [MessageHandler(Filters.text, rules)],

            question: [MessageHandler(Filters.text, question, pass_chat_data=True)],
            # answer: [MessageHandler(Filters.text, answer)],

            one_more: [
                MessageHandler(Filters.regex(r'да'), question),
                MessageHandler(Filters.regex(r'нет'), good_bye),
                MessageHandler(Filters.regex(r''), one_more)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]

    )

    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
