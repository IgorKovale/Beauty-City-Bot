from environs import env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from first_message import start

env.read_env()


def main():
    tg_token = env.str('TG_BOT_TOKEN')

    updater = Updater(tg_token)

    dp = updater.dispatcher
    # Команда /start - выводит пользовательское соглашение
    dp.add_handler(CommandHandler("start", start))

    print("Бот запущен...")
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
