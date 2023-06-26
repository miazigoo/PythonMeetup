from aiogram import types


def get_keyboard_for_start_speakers(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="👁Посмотреть программу мероприятия",
                                   callback_data=callback_keyboard.new(action="view_event", value="", info="")),
        types.InlineKeyboardButton(text="👀 Посмотреть ближайшие мероприятия",
                                   callback_data=callback_keyboard.new(
                                       action="view_upcoming_events", value="", info="")),
        types.InlineKeyboardButton(text="❔Задать вопрос спикеру",
                                   callback_data=callback_keyboard.new(action="ask_question", value="", info="")),
        types.InlineKeyboardButton(text="🤖 Что умеет бот",
                                   callback_data=callback_keyboard.new(action="FAQ", value="", info="")),
        types.InlineKeyboardButton(text="▶️ Начать выступление",
                                   callback_data=callback_keyboard.new(action="start_performance", value="", info="")),
        types.InlineKeyboardButton(text="❌ Закончить выступление",
                                   callback_data=callback_keyboard.new(action="end_performance", value="", info="")),
        types.InlineKeyboardButton(text="📖 Читать вопросы",
                                   callback_data=callback_keyboard.new(action="read_questions", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_back_and_next_question(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value="", info="")),
        types.InlineKeyboardButton(text="🔜 Следующий вопрос",
                                   callback_data=callback_keyboard.new(action="next_question", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard
