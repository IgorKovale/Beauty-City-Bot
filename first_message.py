from environs import env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def start(update: Update, context: CallbackContext):
    with open('documents/Пользовательское_соглашение.pdf', 'rb') as pdf_file:
        update.message.reply_document(
            document=pdf_file,
            filename='Пользовательское_соглашение.pdf'
        )

    keyboard = [[InlineKeyboardButton('Ознакомился!', callback_data='1')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Перед работой мы вынуждены Вас попросить ознакомиться с пользовательским соглашением 🤓', reply_markup=reply_markup)