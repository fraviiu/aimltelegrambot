import config
import constants
import aiml
import telebot

kernel = aiml.Kernel()
kernel.bootstrap(learnFiles=config.startup_file, commands="LOAD AIML BOT")

telebot.apihelper.proxy = {'https': 'socks5://telegram:telegram@ailtn.tgvpnproxy.me:1080'}

bot = telebot.TeleBot(config.token)

is_silenced = False


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


@bot.message_handler(func=lambda message: True, content_types=["text"])
def response(message):
    global is_silenced
    if message.text == "silence_all" or message.text == "SILENCE_ALL":
        is_silenced = True
    if message.text == "unsilence_all" or message.text == "UNSILENCE_ALL":
        is_silenced = False
        return
    if is_silenced:
        return
    response_text = kernel.respond(message.text, message.chat.id)
    bot.send_message(message.chat.id, response_text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
