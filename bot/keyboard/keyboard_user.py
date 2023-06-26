from aiogram import types

from bot.models import Event


def get_keyboard_for_start(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="Посмотреть программу мероприятия",
                                   callback_data=callback_keyboard.new(action="view_event", value="", info="")),
        types.InlineKeyboardButton(text="Посмотреть ближайшие мероприятия",
                                   callback_data=callback_keyboard.new(
                                       action="view_upcoming_events", value="", info="")),
        types.InlineKeyboardButton(text="Задать вопрос спикеру",
                                   callback_data=callback_keyboard.new(action="ask_question", value="", info="")),
        types.InlineKeyboardButton(text="Что умеет бот",
                                   callback_data=callback_keyboard.new(action="FAQ", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_all_event(callback_keyboard):
    buttons = []
    for event in Event.objects.all()[:10]:
        buttons.append(
            types.InlineKeyboardButton(text=f"{event.title}",
                                       callback_data=callback_keyboard.new(
                                           action="allevent", value=f"{event.pk}", info="")),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="back", value="", info="")),
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


