import os
import time
from contextlib import suppress
from aiogram.dispatcher.filters.state import StatesGroup, State
from asgiref.sync import sync_to_async

from bot.keyboard.inline_keyboard import *
from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified

from bot.management.commands.bot import *
from bot.models import Speaker, Client, Question, Event

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

callback_keyboard = CallbackData("procedures", "action", "value", "info")
today = datetime.datetime.today()
user_data = {}

TEXT_NEWSLETTER = 'Запишите сообщение которое хотите разослать. \n' \
                  'Сообщение поддерживает форматирование текста\n'


class PersonalData(StatesGroup):
    waiting_make_newsletter_for_speakers = State()
    waiting_make_newsletter_for_all = State()
    waiting_title_event = State()
    waiting_text_event = State()
    waiting_data_event = State()
    waiting_speaker_time = State()
    waiting_speaker = State()
    waiting_speaker_topic = State()
    waiting_performance_program_time = State()


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard), parse_mode="Markdown")


@sync_to_async()
def get_speakers():
    return list(Speaker.objects.all())


@sync_to_async()
def get_all():
    return list(Client.objects.all())


@sync_to_async()
def get_speaker(telegram_id):
    client = Client.objects.get(telegram_id=telegram_id)
    return Speaker.objects.get(client=client)


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def make_newsletter(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "make_newsletter":
        await update_text(call.message, 'Выберите кому отправить рассылку:', get_keyboard_choose_make_newsletter)
    elif action == "make_newsletter_for_speakers":
        await update_text(call.message, TEXT_NEWSLETTER, get_keyboard_none)
        await state.set_state(PersonalData.waiting_make_newsletter_for_speakers.state)
    elif action == "make_newsletter_for_all":
        await update_text(call.message, TEXT_NEWSLETTER, get_keyboard_none)
        await state.set_state(PersonalData.waiting_make_newsletter_for_all.state)

    elif action == "send_clients":
        newsletter = USERS_DATA.get('newsletter')
        clients = await get_all()
        for client in clients:
            await update_text(call.message, 'wait', get_keyboard_none)
            time.sleep(1)
            try:
                await call.message.bot.send_message(chat_id=int(client.telegram_id), text=newsletter)
            except:
                continue
            time.sleep(1)
        await update_text(call.message, 'ok', get_keyboard_none)
    elif action == "send_speakers":
        newsletter = USERS_DATA.get('newsletter')
        speakers = await get_speakers()
        for speaker in speakers:
            tg_id = int(speaker.client.telegram_id)
            await update_text(call.message, 'Отправляем', get_keyboard_none)
            time.sleep(1)
            try:
                await call.message.bot.send_message(chat_id=tg_id, text=newsletter)
            except:
                continue
            time.sleep(1)
        await update_text(call.message, 'Готово, Мастер!', get_keyboard_none)
    elif action == "cancel":
        text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


async def make_newsletter_for_all(message: types.Message, state: FSMContext):
    newsletter = message.text
    USERS_DATA['newsletter'] = newsletter
    await message.answer(f"Ваше сообщение:\n{newsletter}", reply_markup=get_keyboard_sender_client(callback_keyboard))
    await state.finish()


async def make_newsletter_for_speakers(message: types.Message, state: FSMContext):
    newsletter = message.text
    USERS_DATA['newsletter'] = newsletter
    await message.answer(f"Ваше сообщение:\n{newsletter}", reply_markup=get_keyboard_sender_speakers(callback_keyboard))
    await state.finish()


async def organize_an_event(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    if action == "organize_an_event":
        text = 'Введите название мероприятия:'
        await update_text(call.message, text, get_keyboard_none)
        await state.set_state(PersonalData.waiting_title_event.state)


async def get_title_event(message: types.Message, state: FSMContext):
    await state.update_data(title_event=message.text)

    await state.set_state(PersonalData.waiting_text_event.state)
    await message.answer("Теперь введите описание мероприятия:")


async def get_text_event(message: types.Message, state: FSMContext):
    await state.update_data(text_event=message.text)

    await state.set_state(PersonalData.waiting_data_event.state)
    await message.answer("Теперь укажите дату проведения мероприятия в формате:\n"
                         "*12.06.2024*", parse_mode="Markdown")


async def get_data_event(message: types.Message, state: FSMContext):
    await state.update_data(data_event=message.text)

    await state.set_state(PersonalData.waiting_speaker_time.state)
    await message.answer("Теперь укажите время выступления спикера в формате:\n"
                         "*15:30*", parse_mode="Markdown")


async def get_time_for_speaker_event(message: types.Message, state: FSMContext):
    await state.update_data(time_for_speaker_event=message.text)

    # await state.set_state(PersonalData.waiting_speaker.state)
    await message.answer("Выберите спикера:", reply_markup=get_keyboard_choose_speaker(callback_keyboard))


async def choose_speaker(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    value = callback_data["value"]
    start = user_data.get('start', 10)
    end = user_data.get('end', 20)
    if action == "choose_speaker":
        telegram_id = int(value)
        await state.update_data(choose_speaker_telegram_id=telegram_id)
        text = 'Выберите тему:'
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_choose_topic(callback_keyboard))
    elif action == "choose_speaker_next":
        user_data['start'] = start + 10
        user_data['end'] = end + 10
        await call.message.edit_text("Выберите спикера:",
                                     reply_markup=get_keyboard_choose_speaker_next(callback_keyboard, start, end))
    elif action == "back_choose_speaker":
        user_data['start'] = start - 10
        user_data['end'] = end - 10
        await call.message.edit_text("Выберите спикера:",
                                     reply_markup=get_keyboard_choose_speaker_next(callback_keyboard, start, end))


@sync_to_async()
def create_event(pk, telegram_id, time_event, date, title, text):
    speaker = Speaker.objects.get(client__telegram_id=telegram_id)
    topic, _ = Topic.objects.update_or_create(pk=pk,
                                              defaults={
                                                  'time_event': time_event
                                              })
    event, create = Event.objects.update_or_create(
        date=date,
        defaults={
            'title': title,
            'text': text,
        }
    )
    event.speaker.add(speaker)
    event.topic.add(topic)
    event.save()
    if create:
        event = Event.objects.filter(
            date=date, title=title)[0]
        event.speaker.add(speaker.pk)
        event.topic.add(topic.pk)
        event.save()

    return event


async def choose_topic(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    value = callback_data["value"]
    start_topic = user_data.get('start_topic', 10)
    end_topic = user_data.get('end_topic', 20)
    if action == "choose_topic":
        admin_data = await state.get_data()
        topic_pk = int(value)
        telegram_id = int(admin_data['choose_speaker_telegram_id'])
        time_event = admin_data['time_for_speaker_event'].split(':')
        time_event = datetime.time(int(time_event[0]), int(time_event[1]))
        date = admin_data['data_event'].split('.')
        date = datetime.date(int(date[2]), int(date[1]), int(date[0]))
        title = admin_data['title_event']
        text = admin_data['text_event']
        event = await create_event(topic_pk, telegram_id, time_event, date, title, text)
        print(event)
        await state.update_data(choose_topic_pk=topic_pk)
        text = 'Мероприятие сохранено.'
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_admin_back_and_add(callback_keyboard))
    elif action == "choose_topic_next":
        user_data['start_topic'] = start_topic + 10
        user_data['end_topic'] = end_topic + 10
        await call.message.edit_text("Выберите тему:",
                                     reply_markup=get_keyboard_choose_topic_next(
                                         callback_keyboard, start_topic, end_topic))
        # await update_text(call.message, "Выберите спикера:", get_keyboard_choose_speaker_next)
        # await state.set_state(PersonalData.waiting_title_event.state)
    elif action == "back_choose_topic":
        user_data['start_topic'] = start_topic - 10
        user_data['end_topic'] = end_topic - 10
        await call.message.edit_text("Выберите тему:",
                                     reply_markup=get_keyboard_choose_topic_next(
                                         callback_keyboard, start_topic, end_topic))
    elif action == "admin_add":
        await state.set_state(PersonalData.waiting_speaker_time.state)
        await call.message.answer("Теперь укажите время выступления спикера в формате:\n"
                                  "*15:30*", parse_mode="Markdown")


@sync_to_async()
def view_speakers():
    speakers = Speaker.objects.all()

    return ''.join([f'{speaker.name}\n' for speaker in speakers])


async def admin_view_speakers(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "view_speakers":
        text = '*Все спикеры:*\n'
        text = text + await view_speakers()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


async def applications_for_speakers(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    value = callback_data["value"]
    if action == "applications_for_speakers":
        text = '*Заявки:*\n'
        await update_text(call.message, text, get_keyboard_applications_for_speakers)
    await call.answer()


@sync_to_async()
def add_speaker_topic():
    telegram_id = USERS_DATA.get('application_telegram_id')
    client = Client.objects.get(telegram_id=telegram_id)
    Speaker.objects.update_or_create(client=client,
                                     defaults={
                                         'name': USERS_DATA['speaker_name'],
                                     })
    Topic.objects.update_or_create(title=USERS_DATA['topic_title'])
    application = ApplicationSpeaker.objects.get(client=client)
    application.delete()

    return 'ok'


@sync_to_async()
def delete_application():
    telegram_id = USERS_DATA.get('application_telegram_id')
    client = Client.objects.get(telegram_id=telegram_id)
    ApplicationSpeaker.objects.get(client=client).delete()

    return 'ok'


async def application(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    value = callback_data["value"]
    info = callback_data["info"]
    if action == "applications":
        applications = USERS_DATA.get('topic_title')
        telegram_id = int(value)
        USERS_DATA['application_telegram_id'] = telegram_id
        USERS_DATA['speaker_name'] = info
        text = f'*Заявка от:* {info}\nТема: {applications}'
        await update_text(call.message, text, get_keyboard_add_applications)
    elif action == "add_in_speakers":
        await add_speaker_topic()
        text = 'Спикер и тема *добавлены*'
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_admin_back(callback_keyboard), parse_mode="Markdown")
    elif action == "cancel_application":
        await delete_application()
        text = 'Заявка *отменена*'
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_admin_back(callback_keyboard), parse_mode="Markdown")
    await call.answer()


async def admin_callbacks_back(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "admin_back":
        user_data['start'] = 10
        user_data['end'] = 20
        user_data['start_topic'] = 10
        user_data['end_topic'] = 20
        USERS_DATA.clear()
        text = 'Приветствую, Мастер! Что вы хотите сделать❓'  # await get_start_text()
        await update_text(call.message, text, get_keyboard_admin)
    await call.answer()


async def change_performance_program(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    value = callback_data["value"]
    if action == "change_performance_program":
        text = '*Выберите мероприятие:*'
        await update_text(call.message, text, get_keyboard_change_performance_program)
    elif action == "performance_program":
        event_pk = int(value)
        text = '*Выберите программу в которой необходимо изменить время выступления спикера:*'
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_performance_program(
                                         callback_keyboard, event_pk), parse_mode="Markdown")
    elif action == "program_pk":
        USERS_DATA['program_pk'] = value
        text = "Укажите время выступления спикера в формате:\n*15:30*"
        await state.set_state(PersonalData.waiting_performance_program_time.state)
        await call.message.edit_text(text,
                                     reply_markup=get_keyboard_admin_back(callback_keyboard), parse_mode="Markdown")
    await call.answer()


@sync_to_async()
def performance_program_time_event(time_event):
    topic_pk = USERS_DATA.get('program_pk')
    topic = Topic.objects.get(pk=topic_pk)
    topic.time_event = time_event
    topic.save()

    return 'ok'


async def performance_program_time(message: types.Message, state: FSMContext):
    await state.update_data(waiting_performance_program_time=message.text)
    time_event = message.text.split(':')
    time_event = datetime.time(int(time_event[0]), int(time_event[1]))
    await performance_program_time_event(time_event)
    text = 'Время выступления спикера изменено'
    await message.answer(text, reply_markup=get_keyboard_admin_back(callback_keyboard))


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_newsletter_for_all, state=PersonalData.waiting_make_newsletter_for_all)
    dp.register_message_handler(make_newsletter_for_speakers, state=PersonalData.waiting_make_newsletter_for_speakers)
    dp.register_message_handler(get_title_event, state=PersonalData.waiting_title_event)
    dp.register_message_handler(get_text_event, state=PersonalData.waiting_text_event)
    dp.register_message_handler(get_data_event, state=PersonalData.waiting_data_event)
    dp.register_message_handler(get_time_for_speaker_event, state=PersonalData.waiting_speaker_time)
    dp.register_message_handler(performance_program_time, state=PersonalData.waiting_performance_program_time)

    dp.register_callback_query_handler(
        change_performance_program,
        callback_keyboard.filter(action=[
            "change_performance_program",
            "performance_program",
            "program_pk",
        ]
        ),
        state="*", )

    dp.register_callback_query_handler(
        make_newsletter,
        callback_keyboard.filter(action=[
            "make_newsletter",
            "make_newsletter_for_speakers",
            "make_newsletter_for_all",
            "send_clients",
            "send_speakers",
            "cancel",
        ]
        ),
        state="*", )
    dp.register_callback_query_handler(
        organize_an_event,
        callback_keyboard.filter(action=[
            "organize_an_event",
        ]
        ),
        state="*", )
    dp.register_callback_query_handler(
        applications_for_speakers,
        callback_keyboard.filter(action=[
            "applications_for_speakers",
        ]
        ),
        state="*", )

    dp.register_callback_query_handler(
        application,
        callback_keyboard.filter(action=[
            "applications",
            "add_in_speakers",
            "cancel_application",
        ]
        ),
        state="*", )

    dp.register_callback_query_handler(
        admin_callbacks_back,
        callback_keyboard.filter(action=[
            "admin_back",
        ]
        ),
        state="*", )
    dp.register_callback_query_handler(
        admin_view_speakers,
        callback_keyboard.filter(action=[
            "view_speakers",
        ]
        ),
        state="*", )
    dp.register_callback_query_handler(
        choose_speaker,
        callback_keyboard.filter(action=[
            "choose_speaker",
            "choose_speaker_next",
            "back_choose_speaker",
            # "choose_speaker",
        ]
        ),
        state="*", )
    dp.register_callback_query_handler(
        choose_topic,
        callback_keyboard.filter(action=[
            "choose_topic",
            "choose_topic_next",
            "back_choose_topic",
            "admin_add",
        ]
        ),
        state="*", )
