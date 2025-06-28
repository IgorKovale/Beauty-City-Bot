import sqlite3
import telebot
from environs import env
from database import add_sign_up, get_salons, get_services

env.read_env()
tg_key = env.str('TG_BOT_TOKEN')
bot = telebot.TeleBot(tg_key)

temporary_storage = {}


@bot.message_handler(commands=['sign_up'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Записаться на услугу', 'Мои записи')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Записаться на услугу')
def choose_salon(message):
    salons = get_salons()
    markup = telebot.types.InlineKeyboardMarkup()
    for salon in salons:
        button = telebot.types.InlineKeyboardButton(text=salon[2], callback_data=f'salon_{salon[0]}')
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите салон:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('salon_'))
def choose_service(call):
    salon_id = call.data.split('_')[1]
    temporary_storage['salon_id'] = salon_id
    services = get_services()
    markup = telebot.types.InlineKeyboardMarkup()
    for service in services:
        button = telebot.types.InlineKeyboardButton(text=f'Услуга : {service[1]}, Цена : {service[2]} Р',
                                                    callback_data=f'service_{service[0]}')
        markup.add(button)
    bot.send_message(call.message.chat.id, "Выберите услугу:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def choose_datetime(call):
    service_id = call.data.split('_')[1]
    temporary_storage['service_id'] = service_id
    bot.send_message(call.message.chat.id, "Напишите время:")

bot.polling()
