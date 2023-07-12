import telebot
from config import keys, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Для того чтобы начать работу введите команду боту в следующем\
     формате:\n<имя конвертируемой валюты> <имя валюты,\
 в которую необходимо конвертировать исходную валюту> <количество первой \
 валюты>\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message,text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()
        if len(values) > 3:
            raise APIException(f'Слишком много параметров')
        quote, base, amount = values
        total_price = CurrencyConverter.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n/help')
    else:
        text = f'Цена за {amount} {keys[quote]} в {keys[base]} : {total_price}'
        bot.send_message(message.chat.id,text)

bot.polling(none_stop=True)

