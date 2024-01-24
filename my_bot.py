import telebot
from config import keys, TOKEN, start, help
from utils import ConvertationException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['menu'])
def main_menuu(message):
    bot.send_message(message.chat.id, start)


@bot.message_handler(commands=['start'])
def startt(message):
    bot.send_message(message.chat.id, help + '\n /menu')


@bot.message_handler(commands=['help'])
def helpp(message):
    bot.send_message(message.chat.id, help + '\n /menu')


@bot.message_handler(commands=['keys'])
def keyss(message):
    bot.send_message(message.chat.id, 'ДОСТУПНЫ СЛЕДУЮЩИЕ ВАЛЮТЫ:')
    for i in keys:
        bot.send_message(message.chat.id, i + ' ' + keys[i])
    bot.send_message(message.chat.id, '/menu')


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertationException('Слишком много или слишком мало параметров')

        quote, base, amount = values
        total_base = CryptoConverter.converter(quote, base, amount)
    except ConvertationException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f'{amount} {keys[base]}({base}) в {keys[quote]}({quote}) равно: {total_base}'
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "/menu")


bot.polling(none_stop=True)
