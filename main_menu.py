from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("Записаться к любимому мастеру", callback_data="choose_master"),
        InlineKeyboardButton("Записаться на процедуру", callback_data="choose_service"),
        InlineKeyboardButton("Записаться через салон", callback_data="choose_salon"),
        InlineKeyboardButton("Записаться по номеру телефона", callback_data="by_phone")
    )
    return markup


def show_main_menu(bot, chat_id):
    """Показывает меню с 4 кнопками"""
    markup = create_menu()
    bot.send_message(
        chat_id=chat_id,
        text="Выберите способ записи:",
        reply_markup=markup
    )
