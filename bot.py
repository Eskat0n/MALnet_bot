from urllib.request import urlretrieve

import telebot
from telebot.types import InlineQueryResultArticle
from emoji import emojize

import mal
from config import read_bot_config


class MALnetBot(telebot.TeleBot):
    def __init__(self):
        super().__init__(read_bot_config()['Token'])

        self.add_message_handler(self.send_help,
                                 commands=['start', 'help'])
        self.add_message_handler(self.chat_send_search_entries,
                                 func=lambda m: True)

        self.add_inline_handler(self.inline_send_search_entries,
                                func=lambda q: True)

    def send_help(self, message):
        pass

    def chat_send_search_entries(self, message):
        chat_id = message.chat.id
        entries = self.search_entries(message.text)

        if len(entries) == 0:
            self.send_message(chat_id,
                              text=emojize("Nothing found :cry:", use_aliases=True),
                              disable_notification=True)
        else:
            self.send_entry(chat_id, entries[0])

    def inline_send_search_entries(self, query):
        entries = self.search_entries(query.query)
        results = [InlineQueryResultArticle(entry.id, entry.title, entry.to_markdown,
                                            parse_mode='Markdown',
                                            disable_web_page_preview=True,
                                            thumb_url=entry.image,
                                            description=entry.score_info)
                   for entry in entries[0:5]]

        self.answer_inline_query(query.id, results)

    def send_entry(self, chat_id, entry):
        filename = '{}.jpg'.format(entry.id)
        urlretrieve(entry.image, filename)
        image = open(filename, 'rb')

        self.send_photo(chat_id,
                        photo=image,
                        disable_notification=True)
        self.send_message(chat_id,
                          text=entry.to_markdown,
                          parse_mode='Markdown',
                          disable_web_page_preview=True,
                          disable_notification=True)

    def run(self):
        self.polling()

    @staticmethod
    def search_entries(text):
        words = text.split(' ')
        if words[0] in ['m', 'manga']:
            return mal.search_manga(' '.join(words[1:]))
        else:
            return mal.search_anime(text)


if __name__ == '__main__':
    bot = MALnetBot()
    bot.run()
