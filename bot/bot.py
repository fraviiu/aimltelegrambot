import config
import constants
import aiml
import telebot
import random
from googletrans import Translator
import os

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="aiml/startup.xml", commands="LOAD AIML BOT")

translator = Translator()

# telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@ailtn.tgvpnproxy.me:1080'}

# token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(config.token)

is_silenced = False


def translate_text(text, dest):
    if text == "":
        text = random.choice(constants.random_russian_words)
        response_text = constants.empty_translate_text_message.format(
            text,
            translator.translate(text, dest=dest).text
        )
    else:
        response_text = translator.translate(text, dest=dest).text
    return response_text


@bot.message_handler(commands=["silence"])
def handle_start(message):
    global is_silenced
    is_silenced = True
    bot.send_message(message.chat.id, "Молчу :(")


@bot.message_handler(commands=["unsilence"])
def handle_start(message):
    global is_silenced
    is_silenced = False
    bot.send_message(message.chat.id, "Ура! Я могу говорить!")


@bot.message_handler(commands=["start"])
def handle_start(message):
    if is_silenced:
        return
    bot.send_message(message.chat.id, constants.title_ru)


@bot.message_handler(commands=["help"])
def handle_help(message):
    if is_silenced:
        return
    bot.send_message(message.chat.id, constants.help_ru)


@bot.message_handler(commands=["report"])
def handle_help(message):
    if is_silenced:
        return
    bot.send_message(message.chat.id, constants.random_speech)


@bot.message_handler(commands=["translate"])
def handle_translate(message):
    if is_silenced:
        return
    command_len = len("/translate") + 1

    text = message.text[command_len:]
    dest_lang = kernel.getPredicate("translate_dest_lang", message.chat.id)
    dest_lang = dest_lang if dest_lang in constants.languages else "en"

    if text[:2] in constants.languages:
        dest_lang = text[:2]
        text = text[3:]
    response_text = translate_text(text, dest=dest_lang)
    bot.send_message(message.chat.id, response_text)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def response(message):
    global is_silenced
    if message.text == "silence_all" or message.text == "SILENCE_ALL":
        is_silenced = True
    if message.text == "unsilence_all" or message.text == "UNSILENCE_ALL":
        is_silenced = False
        return
    if message.text == "report_all" or message.text == "REPORT_ALL":
        bot.reply_to(message, constants.random_speech)
        return
    if is_silenced:
        return
    response_text = kernel.respond(message.text + "1", message.chat.id)
    bot.reply_to(message, response_text)


if __name__ == '__main__':
    bot.polling(none_stop=True)


