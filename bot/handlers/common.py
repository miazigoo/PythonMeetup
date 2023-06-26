from contextlib import suppress

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, IDFilter
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.keyboard.inline_keyboard import get_keyboard_admin, USERS_DATA
from bot.keyboard.keyboard_speaker import get_keyboard_for_start_speakers

from bot.keyboard.keyboard_user import get_keyboard_for_start
from bot.models import Client, Speaker

callback_keyboard = CallbackData("procedures", "action", "value", "info")
START_TEXT = "Вас приветствует Сервис PythonMeetup"


# @sync_to_async()
def get_speakers_id():
    speakers = Speaker.objects.all()
    speakers_id = []
    for speaker in speakers:
        speakers_id.append(speaker.client.telegram_id)
    return speakers_id


SPEAKERS_ID = get_speakers_id()


async def update_text_fab(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


# @sync_to_async()
# def get_start_text():
#     about_us = StartText.objects.filter(pk=1)
#     if about_us:
#         text = about_us[0].descriptions
#     else:
#         text = START_TEXT['start_text']
#
#     return text


@sync_to_async()
def get_and_create_client(telegram_id):
    client, _ = Client.objects.update_or_create(
        telegram_id=USERS_DATA[f'{telegram_id}']['telegram_id'],
        defaults={
            'nik_name': USERS_DATA[f'{telegram_id}']['nikname'],
        }
    )
    return client


# Хэндлер на команду /start
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    telegram_id = message.from_id
    nikname = message.from_user.username
    USERS_DATA[f'{telegram_id}'] = {'telegram_id': telegram_id,
                                    'nikname': nikname
                                    }
    await get_and_create_client(telegram_id)
    text = START_TEXT  # await get_start_text()
    # speakers_id = await get_speakers_id()
    keyboard = get_keyboard_for_start(callback_keyboard)
    if telegram_id in SPEAKERS_ID:
        keyboard = get_keyboard_for_start_speakers(callback_keyboard)
    await message.answer(
        text,
        reply_markup=keyboard
    )


# Хэндлер на команду /cancel
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


# Хэндлер на команду /admin
async def cmd_admin(message: types.Message, state: FSMContext):
    await state.finish()
    text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
    await message.answer(
        text,
        reply_markup=get_keyboard_admin(callback_keyboard)
    )


# Просто функция, которая доступна только администратору,
# чей ID указан в файле конфигурации.
async def secret_command(message: types.Message):
    await message.answer("Поздравляю! Эта команда доступна только администратору бота.")


def register_handlers_common(dp: Dispatcher, admin_id: int):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(secret_command, IDFilter(user_id=admin_id), commands="abracadabra")
    dp.register_message_handler(cmd_admin, IDFilter(user_id=admin_id), commands="admin", state="*")
