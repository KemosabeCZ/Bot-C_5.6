import telebot
from C_5_6_Bot_extensions import APIException, Converter
from C_5_6_Bot_config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Приветствую Вас!\n ' \
           'Конвертация валют осуществляется\n' \
           'по текущим курсам Центробанка ЕС.\n' \
           'Для дальнейшей работы используйте  /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны операции с:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    text2 = 'Введите через пробел:\n' \
            'Сколько конвертируем, что конвертируем, во что конвертируем'
    bot.reply_to(message, text)
    bot.reply_to(message, text2)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Converter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
