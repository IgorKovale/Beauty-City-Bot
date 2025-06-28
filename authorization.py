from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user, check_user_exists
from main_menu import show_main_menu


temporary_storage = {}


def setup_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        msg = bot.send_message(message.chat.id, 'Введите ваше имя:')
        bot.register_next_step_handler(msg, process_name)

    def process_name(message):
        user_id = message.from_user.id
        temporary_storage[user_id] = {'name': message.text}

        msg = bot.send_message(message.chat.id, 'Введите ваш номер телефона:')
        bot.register_next_step_handler(msg, process_phone)

    def process_phone(message):
        user_id = message.from_user.id
        phone = message.text

        # Если авторизован выводим меню
        if check_user_exists(phone):
            bot.send_message(message.chat.id, 'Мы Вас помнили 😉')
            show_main_menu(bot, message.chat.id)
            return

        temporary_storage[user_id]['phone'] = phone

        with open('documents/Пользовательское_соглашение.pdf', 'rb') as doc:
            bot.send_document(
                chat_id=message.chat.id,
                document=doc,
                caption='Перед работой мы вынуждены Вас попросить ознакомиться с пользовательским соглашением 🤓',
                reply_markup=create_confirmation_button(user_id)
            )

    def create_confirmation_button(name):
        # создать кнопку
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('✅ Ознакомился', callback_data=f'accept_{name}'))
        return markup

    @bot.callback_query_handler(func=lambda call: call.data.startswith('accept_'))
    def handle_agreement(call):
        user_id = int(call.data.split('_')[1])
        user_data = temporary_storage.get(user_id)

        if user_data:
            add_user(user_data['name'], user_data['phone'])
            del temporary_storage[user_id]

        bot.answer_callback_query(call.id, 'Спасибо что выбрали нас!')

        # Удалить кнопку
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        # Авторизовался, вывод в меню
        show_main_menu(bot, call.message.chat.id)