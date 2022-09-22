import telebot
from config import keys, TOKEN
from extensions import APIException
from extensions import CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message: telebot.types.Message):
    text = f'Здравствуйте, {message.chat.first_name}, я автоконвертер валюты.' \
           f'\nДля конвертации используйте образец параметров:'\
           f'\n<из какой валюты> <в какую валюту> <количество>'\
           f'\nОбразец: Рубль Доллар 25'\
           f'\nНачать работу: /start'\
           f'\nПомощь: /help'\
           f'\nСписок валют: /values'
    print(message.text)
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список валют:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Некорректные данные /help')
        elif len(values) < 3:
            raise APIException('Сверьтесь с образцом. /help')
        else:
            quote, base, amount = values
            total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка конвертации: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать валюту. \n{e}')
    else:
        text = f'{message.chat.first_name}, {amount} {quote} составит {total_base} в валюте {base}.'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)