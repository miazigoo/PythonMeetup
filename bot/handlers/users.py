from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.handlers.common import START_TEXT, SPEAKERS_ID
from bot.keyboard.keyboard_speaker import get_keyboard_for_start_speakers

from bot.keyboard.keyboard_user import get_keyboard_back, get_keyboard_all_event, get_keyboard_for_start
from bot.models import Event, Flag, Question

callback_keyboard = CallbackData("procedures", "action", "value", "info")
EVENT_TEXT = """
Программа на 20.06: 
*Отлоси клоси мафлоси*
----------------------------------------------------------------------------
Будем говорить чепуху целый час.
Ждем всех! Может услышим что-то забавное. 
ДАЕШЬ ЧЕПУХРЕНЬ!!!
"""


class PersonalData(StatesGroup):
    waiting_ask_question = State()


@sync_to_async()
def get_event(pk):
    return Event.objects.get(pk=pk)


@sync_to_async()
def chek_speaker():
    speaker = Flag.objects.filter(flag=True)
    speaker_now = None
    if speaker:
        # topic = speaker[0].speaker.topic.title
        speaker_now = f"""
Сейчас выступает *{speaker[0].speaker.name}*.
Задайте интересующий вас вопрос сообщением:
"""
    return speaker, speaker_now


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard), parse_mode="Markdown")


async def start_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "view_event":
        pk = 1
        event = await get_event(pk)
        if event:
            display_topics = event.display_topics()
            text = f'{event.title}\n' \
                   f'{event.text}\n' \
                   f'{display_topics}'
        # text = EVENT_TEXT
        else:
            text = EVENT_TEXT
        await update_text(call.message, text, get_keyboard_back)
    elif action == "view_upcoming_events":
        text = '# ---------------------------------------\n' \
               '# ближайшие мероприятия\n' \
               '# ---------------------------------------'
        await update_text(call.message, text, get_keyboard_all_event)
    elif action == "ask_question":
        speaker, speaker_now = await chek_speaker()
        if speaker:
            await update_text(call.message, speaker_now, get_keyboard_back)
            await state.set_state(PersonalData.waiting_ask_question.state)
        else:
            text = "🤷‍♂️Сейчас никто не выступает\nДождитесь начала выступления."
            await update_text(call.message, text, get_keyboard_back)

    await call.answer()


async def view_event(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    value = callback_data["value"]
    if action == "allevent":
        pk = int(value)
        event = await get_event(pk)
        display_topics = event.display_topics()
        text = f'{event.title}\n' \
               f'{event.text}\n' \
               f'➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n' \
               f'{display_topics}\n'
        # text = EVENT_TEXT
        await update_text(call.message, text, get_keyboard_back)

    await call.answer()


@sync_to_async()
def add_question(question, user):
    speaker = Flag.objects.filter(flag=True)
    if speaker:
        speaker = speaker[0].speaker
        Question.objects.create(
            speaker=speaker,
            text=question,
            nikname=user
        )
    return speaker


async def send_question(message: types.Message, state: FSMContext):
    newsletter = message.text
    user = message.from_user.username
    await add_question(newsletter, user)
    await message.answer(f"✅ Ваше сообщение:\n{newsletter} отправлено",
                         reply_markup=get_keyboard_back(callback_keyboard))
    await state.finish()


async def callbacks_back(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    telegram_id = call.from_user.id
    if action == "back":
        keyboard = get_keyboard_for_start
        if telegram_id in SPEAKERS_ID:
            keyboard = get_keyboard_for_start_speakers
        text = START_TEXT
        await update_text(call.message, text, keyboard)
    await call.answer()


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(send_question, state=PersonalData.waiting_ask_question)
    # dp.register_message_handler(make_newsletter_for_speakers, state=PersonalData.waiting_make_newsletter_for_speakers)

    dp.register_callback_query_handler(
        start_callback,
        callback_keyboard.filter(action=[
            "view_event",
            "view_upcoming_events",
            "ask_question",
        ]),
        state="*", )
    dp.register_callback_query_handler(
        view_event,
        callback_keyboard.filter(action=[
            "allevent",
        ]),
        state="*", )
    dp.register_callback_query_handler(
        callbacks_back,
        callback_keyboard.filter(action=[
            "back",
        ]),
        state="*", )
