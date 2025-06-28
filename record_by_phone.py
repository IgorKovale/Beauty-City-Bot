from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from main_menu import show_main_menu


def setup_by_phone_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == 'by_phone')
    def handle_by_phone(call):

        salon_phone = '+7 (800) 555-35-35'

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('⬅️ Назад', callback_data='back_to_menu'))

        bot.send_message(
            chat_id=call.message.chat.id,
            text=f'Вы можете записаться по телефону:\n'
                 f'{salon_phone}\n'
                 f'Наш администратор поможет вам с выбором времени и процедуры.',
            reply_markup=markup
        )
    @bot.callback_query_handler(func=lambda call: call.data == 'back_to_menu')
    def handle_back_to_menu(call):
        """Удаляем текст и возвращаемся в меню"""
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # Не уверен, стоит ли удалять
        show_main_menu(bot, call.message.chat.id)