from urllib.request import urlretrieve

import telebot
from telebot.types import InlineQueryResultArticle
from emoji import emojize

import mal
from config import read_bot_config

bot_config = read_bot_config()
bot = telebot.TeleBot(bot_config['Token'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    pass


@bot.message_handler(func=lambda m: True)
def search_anime(message):
    chat_id = message.chat.id
    entries = mal.search_anime(message.text)

    if len(entries) == 0:
        bot.send_message(chat_id,
                         text=emojize("Nothing found :cry:", use_aliases=True),
                         disable_notification=True)
    else:
        send_anime(chat_id, entries[0])

@bot.inline_handler(func=lambda q: True)
def query_text(query):
    entries = mal.search_anime(query.query)
    results = [InlineQueryResultArticle(entry.id, entry.title, entry.to_markdown,
                                        parse_mode='Markdown',
                                        disable_web_page_preview=True,
                                        thumb_url=entry.image,
                                        description=entry.score_info)
               for entry in entries[0:5]]

    bot.answer_inline_query(query.id, results)


def send_anime(chat_id, entry):
    filename = '{}.jpg'.format(entry.id)
    urlretrieve(entry.image, filename)
    image = open(filename, 'rb')

    bot.send_photo(chat_id,
                   photo=image,
                   disable_notification=True)
    bot.send_message(chat_id,
                     text=entry.to_markdown,
                     parse_mode='Markdown',
                     disable_web_page_preview=True,
                     disable_notification=True)


bot.polling()
