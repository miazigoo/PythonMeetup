from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.keyboard.keyboard_user import get_keyboard_back
from bot.models import ApplicationSpeaker, Client

callback_keyboard = CallbackData("procedures", "action", "value", "info")
USERS_DATA = {}


class PersonalData(StatesGroup):
    waiting_get_speaker_name = State()
    waiting_get_topic = State()


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard))


# Хэндлер на команду /add_speaker
async def add_speakers(message: types.Message, state: FSMContext):
    await state.finish()
    text = 'Приветствую, Мастер! Как вас зовут❓\n' \
           'Отправьте свои ФИО одним сообщением.'
    await message.answer(
        text,
        reply_markup=get_keyboard_back(callback_keyboard)
    )
    await state.set_state(PersonalData.waiting_get_speaker_name.state)


async def get_speaker_name(message: types.Message, state: FSMContext):
    speaker_name = message.text
    user_id = message.from_user.id
    user_nikname = message.from_user.username
    USERS_DATA['speaker_name'] = speaker_name
    USERS_DATA['user_id'] = user_id
    USERS_DATA['nikname'] = user_nikname
    text = f"✅ Уважаемый {speaker_name}\n" \
           'Теперь напишите *тему вашего выступления*:'
    await message.answer(text, reply_markup=get_keyboard_back(callback_keyboard), parse_mode="MarkdownV2")
    await state.set_state(PersonalData.waiting_get_topic.state)


@sync_to_async()
def add_application_speaker(topic):
    speaker = USERS_DATA.get('speaker_name')
    user_id = USERS_DATA.get('user_id')
    nikname = USERS_DATA.get('nikname')
    client, created = Client.objects.get_or_create(
        telegram_id=user_id,
        defaults={
            'nik_name': nikname,
        }
    )
    if created:
        client = Client.objects.get_or_create(
            telegram_id=user_id)
    ApplicationSpeaker.objects.update_or_create(
        client=client,
        defaults={
            "name": speaker,
            "topic": topic,
        }
    )
    return 'OK'


async def get_speaker_topic(message: types.Message, state: FSMContext):
    topic = message.text
    text = f"✅ Ваша заявка *отправлена*"
    await message.answer(text, reply_markup=get_keyboard_back(callback_keyboard), parse_mode="MarkdownV2")
    await add_application_speaker(topic)
    await state.finish()


def register_handlers_add_speakers(dp: Dispatcher):
    dp.register_message_handler(add_speakers, commands="add_speaker", state="*")
    dp.register_message_handler(get_speaker_name, state=PersonalData.waiting_get_speaker_name)
    dp.register_message_handler(get_speaker_topic, state=PersonalData.waiting_get_topic)
