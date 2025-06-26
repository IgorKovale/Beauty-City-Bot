from environs import env
from telebot import TeleBot
from authorization import setup_handlers


env.read_env()


def main():
    tg_token = env.str('TG_BOT_TOKEN')
    bot = TeleBot(tg_token)
    setup_handlers(bot)

    print('Бот взлетел')
    bot.infinity_polling()


if __name__ == '__main__':
    main()
