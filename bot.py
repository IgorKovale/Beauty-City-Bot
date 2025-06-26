import sqlite3
import telebot
from environs import env

env.read_env()
tg_key = env.str('TG_BOT_TOKEN')
bot = telebot.TeleBot(tg_key)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Записаться на услугу', 'Мои записи')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Записаться на услугу')
def choose_salon(message):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM salons")
    salons = cursor.fetchall()
    markup = telebot.types.InlineKeyboardMarkup()
    for salon in salons:
        button = telebot.types.InlineKeyboardButton(text=salon[2], callback_data=f'salon_{salon[0]}')
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите салон:", reply_markup=markup)
    cursor.close()
    conn.close()


@bot.callback_query_handler(func=lambda call: call.data.startswith('salon_'))
def select_salon(call):
    conn = sqlite3.connect('test.db', check_same_thread=False)
    cursor = conn.cursor()
    salon_id = call.data.split('_')[1]
    cursor.execute(f"SELECT * FROM services")
    services = cursor.fetchall()

    markup = telebot.types.InlineKeyboardMarkup()
    for service in services:
        button = telebot.types.InlineKeyboardButton(text=f'Услуга : {service[1]}, Цена : {service[2]} Р',
                                                    callback_data=f'service_{service[0]}_{salon_id}')
        markup.add(button)
    bot.send_message(call.message.chat.id, "Выберите услугу:", reply_markup=markup)


bot.polling()
