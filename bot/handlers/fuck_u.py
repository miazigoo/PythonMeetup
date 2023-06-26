
from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from bot.keyboard.keyboard_user import get_keyboard_back

callback_keyboard = CallbackData("procedures", "action", "value", "info")
FAQ = """
Уважаемые пользователи❗️
ВПЕРВЫЕ‼️
Представляем вашему вниманию нашего бота❗️
Хотите спросить что он умеет⁉️
БОТ УМЕЕТ КАКАТЬ‼️
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
/admin - Меню администратора.
/add_speaker - Подать заявку в спикеры
"""


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


async def fuck_u(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "FAQ":
        await update_text(call.message, FAQ, get_keyboard_back)

    await call.answer()


def register_handlers_fuck_u(dp: Dispatcher):
    dp.register_callback_query_handler(
        fuck_u,
        callback_keyboard.filter(action=[
            "FAQ",
        ]),
        state="*", )
