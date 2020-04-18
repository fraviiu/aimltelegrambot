import constants
import aiml
import telebot
import random
import os

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles="aiml/startup.xml", commands="LOAD AIML BOT")


# telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@ailtn.tgvpnproxy.me:1080'}

token = os.environ['1284275711:AAHQuDfZ6W11ZDKob_yJ9jhD70KVYW2U5lk']
bot = telebot.TeleBot('token')

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


@bot.message_handler(commands=["mute"])
def handle_start(message):
    global is_silenced
    is_silenced = True
    bot.send_message(message.chat.id, "O JOGO PAROU ")


@bot.message_handler(commands=["unmute"])
def handle_start(message):
    global is_silenced
    is_silenced = False
    bot.send_message(message.chat.id, "*Verdade ou Desafio?* !")


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


