from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_confirmation_button():
    # Создание кнопки
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Ознакомился", callback_data="confirmed"))
    return markup


def setup_handlers(bot):
    @bot.message_handler(commands=['start', 'help'])
    def send_agreement(message):
        # Отправка соглашения
        with open('documents/Пользовательское_соглашение.pdf', 'rb') as doc:
            bot.send_document(
                chat_id=message.chat.id,
                document=doc,
                caption='Перед работой мы вынуждены Вас попросить ознакомиться с пользовательским соглашением 🤓',
                reply_markup=create_confirmation_button()
            )

    @bot.callback_query_handler(func=lambda call: call.data == "confirmed")
    def handle_confirmation(call):
        # Убирает кнопку и выводит благодарность
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
        bot.answer_callback_query(call.id, "Спасибо за подтверждение!")
        bot.send_message(call.message.chat.id, "Вы можете продолжать использовать бота")