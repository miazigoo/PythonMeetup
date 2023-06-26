import datetime

from aiogram import types

# from bot.models import Weekend, Salons, Appointments, Employee, Procedures, Client

# from django.utils.timezone import localtime
from bot.models import Speaker, Topic, ApplicationSpeaker, Event

USERS_DATA = {}


def get_keyboard_admin(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Заявки в докладчики",
            callback_data=callback_keyboard.new(action="applications_for_speakers", value="", info="")),
        types.InlineKeyboardButton(
            text="Посмотреть докладчиков",
            callback_data=callback_keyboard.new(action="view_speakers", value="", info="")),
        types.InlineKeyboardButton(
            text="Создать мероприятие 🛃",
            callback_data=callback_keyboard.new(action="organize_an_event", value="", info="")),
        types.InlineKeyboardButton(
            text="Поменять программу выступления",
            callback_data=callback_keyboard.new(action="change_performance_program", value="", info="")),
        types.InlineKeyboardButton(
            text="Сделать рассылку",
            callback_data=callback_keyboard.new(action="make_newsletter", value="", info="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_admin_back(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_admin_back_and_add(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
        types.InlineKeyboardButton(text="➕ Добавить тему и спикера",
                                   callback_data=callback_keyboard.new(action="admin_add", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_sender_client(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Отправить",
            callback_data=callback_keyboard.new(action="send_clients", value="", info="")),
        types.InlineKeyboardButton(
            text="Отменить",
            callback_data=callback_keyboard.new(action="cancel", value="", info="")),

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_sender_speakers(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Отправить",
            callback_data=callback_keyboard.new(action="send_speakers", value="", info="")),
        types.InlineKeyboardButton(
            text="Отменить",
            callback_data=callback_keyboard.new(action="cancel", value="", info="")),

    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_make_newsletter(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Докладчикам",
            callback_data=callback_keyboard.new(action="make_newsletter_for_speakers", value="", info="")),
        types.InlineKeyboardButton(
            text="Всем пользователям бота",
            callback_data=callback_keyboard.new(action="make_newsletter_for_all", value="", info="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_speaker(callback_keyboard):
    buttons = []
    for speaker in Speaker.objects.all()[:10]:
        buttons.append(
            types.InlineKeyboardButton(text=f"{speaker.name}",
                                       callback_data=callback_keyboard.new(
                                           action="choose_speaker", value=f"{speaker.client.telegram_id}"
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    if len(Speaker.objects.all()) >= 10:
        buttons.append(
            types.InlineKeyboardButton(text="➡️ Следующая страница",
                                       callback_data=callback_keyboard.new(
                                           action="choose_speaker_next", value="", info="")),
        )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_speaker_next(callback_keyboard, start, end):
    buttons = []
    for speaker in Speaker.objects.all()[start:end]:
        buttons.append(
            types.InlineKeyboardButton(text=f"{speaker.name}",
                                       callback_data=callback_keyboard.new(
                                           action="choose_speaker", value=f"{speaker.client.telegram_id}", info=""
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    if start > 0:
        buttons.append(
            types.InlineKeyboardButton(text="⬅️ Предыдущая страница",
                                       callback_data=callback_keyboard.new(
                                           action="back_choose_speaker", value="", info="")),
        )
    if len(Speaker.objects.all()) >= end:
        buttons.append(
            types.InlineKeyboardButton(text="➡️ Следующая страница",
                                       callback_data=callback_keyboard.new(
                                           action="choose_speaker_next", value="", info="")),
        )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_topic(callback_keyboard):
    buttons = []
    topics = Topic.objects.all()
    for topic in topics[:10]:
        buttons.append(
            types.InlineKeyboardButton(text=f"{topic.title}",
                                       callback_data=callback_keyboard.new(
                                           action="choose_topic", value=f"{topic.pk}", info=""
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    if len(topics) >= 10:
        buttons.append(
            types.InlineKeyboardButton(text="➡️ Следующая страница",
                                       callback_data=callback_keyboard.new(action="choose_topic_next", value="",
                                                                           info="")),
        )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_choose_topic_next(callback_keyboard, start, end):
    buttons = []
    topics = Topic.objects.all()
    for topic in topics[start:end]:
        buttons.append(
            types.InlineKeyboardButton(text=f"{topic.title}",
                                       callback_data=callback_keyboard.new(
                                           action="choose_topic", value=f"{topic.pk}", info=""
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    if start > 0:
        buttons.append(
            types.InlineKeyboardButton(text="⬅️ Предыдущая страница",
                                       callback_data=callback_keyboard.new(
                                           action="back_choose_topic", value="", info="")),
        )
    if len(topics) >= end:
        buttons.append(
            types.InlineKeyboardButton(text="➡️ Следующая страница",
                                       callback_data=callback_keyboard.new(
                                           action="choose_topic_next", value="", info="")),
        )
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_applications_for_speakers(callback_keyboard):
    buttons = []
    applications = ApplicationSpeaker.objects.all()
    for application in applications:
        buttons.append(
            types.InlineKeyboardButton(text=f"{application.name}",
                                       callback_data=callback_keyboard.new(
                                           action="applications", value=f"{application.client.telegram_id}",
                                           info=f"{application.name}"
                                       )),
        )
        USERS_DATA['topic_title'] = f'{application.topic}'
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_add_applications(callback_keyboard):
    buttons = [
        types.InlineKeyboardButton(
            text="Добавить в докладчики",
            callback_data=callback_keyboard.new(action="add_in_speakers", value="", info="")),
        types.InlineKeyboardButton(
            text="Отменить заявку",
            callback_data=callback_keyboard.new(action="cancel_application", value="", info="")),
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_change_performance_program(callback_keyboard):
    buttons = []
    events = Event.objects.all()
    for event in events:
        buttons.append(
            types.InlineKeyboardButton(text=f"{event.title}",
                                       callback_data=callback_keyboard.new(
                                           action="performance_program", value=f"{event.pk}",
                                           info=""
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_performance_program(callback_keyboard, event_pk):
    buttons = []
    events = Event.objects.get(pk=event_pk)
    for topic in events.topic.all():
        buttons.append(
            types.InlineKeyboardButton(text=f"{topic.title}",
                                       callback_data=callback_keyboard.new(
                                           action="program_pk", value=f"{topic.pk}",
                                           info=""
                                       )),
        )
    buttons.append(
        types.InlineKeyboardButton(text="🔚 В начало",
                                   callback_data=callback_keyboard.new(action="admin_back", value="", info="")),
    )
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


def get_keyboard_none(callback_keyboard):
    buttons = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

# def get_keyboard_start_payment(callback_keyboard):
#     buttons = [
#         types.InlineKeyboardButton(text="💰 Оплатить онлайн",
#                                    url="http://127.0.0.1:8000/pay"),
#         types.InlineKeyboardButton(text="✏️Записаться к нам",
#                                    callback_data=callback_keyboard.new(action="sign_up", value="")),
#         types.InlineKeyboardButton(text="📅 Посмотреть свои записи",
#                                    callback_data=callback_keyboard.new(action="your_recordings", value="")),
#         types.InlineKeyboardButton(text="🪪 О нас",
#                                    callback_data=callback_keyboard.new(action="about_us", value="")),
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value="")),
#         types.InlineKeyboardButton(text="💬 Оставить комментарий",
#                                    url="http://127.0.0.1:8000/comments")
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard


# def get_keyboard_select_procedures(callback_keyboard):
#     procedures = Procedures.objects.all()
#     buttons = []
#     for procedure in procedures:
#         text = procedure.name
#         value = procedure.pk
#         buttons.append(
#             types.InlineKeyboardButton(text=text,
#                                        callback_data=callback_keyboard.new(action="procedure", value=value))
#         )
#     buttons.append(
#         types.InlineKeyboardButton(text="🔚 В начало",
#                                    callback_data=callback_keyboard.new(action="back", value=""))
#     )
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(*buttons)
#     return keyboard
#
#
# def get_keyboard_choose_specialist_before_change_date(callback_keyboard):
#     buttons = []
#     for master in Employee.objects.filter(procedure__pk=int(USERS_DATA["procedures"])):
#         buttons.append(
#             types.InlineKeyboardButton(text=f"✅ Мастер {master.name}",
#                                        callback_data=callback_keyboard.new(action="navigation_calendar",
#                                                                            value=master.pk)),
#         )
#     buttons.append(
#         types.InlineKeyboardButton(text="🔚 В начало",
#                                    callback_data=callback_keyboard.new(action="back", value=""))
#     )
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
#
#
# def get_keyboard_choose_specialist(callback_keyboard):
#     buttons = []
#     date = USERS_DATA.get("date")
#     users_time = datetime.datetime.strptime(USERS_DATA.get("time"), "%H:%M").time()
#     overlays = Appointments.objects.filter(appointment_date=date, appointment_time=users_time)
#     if overlays:
#         overlay = overlays[0]
#     else:
#         overlay = None
#     for master in Employee.objects.filter(procedure__pk=int(USERS_DATA.get("procedures"))):
#         if overlay:
#             if master == overlay.master:
#                 continue
#         buttons.append(types.InlineKeyboardButton(text=f"✅ Мастер {master.name}",
#                                                   callback_data=callback_keyboard.new(action="personal_data",
#                                                                                       value=master.pk)))
#     add_text = ""
#     if not buttons:
#         add_text = "В это время нет свободных мастеров"
#     buttons.append(types.InlineKeyboardButton(text=f"{add_text} 🔚 В начало",
#                                               callback_data=callback_keyboard.new(action="back", value="")))
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard


# def get_keyboard_sign_up(callback_keyboard):
#     buttons = [
#         types.InlineKeyboardButton(
#             text="🕔 Записаться на удобное время",
#             callback_data=callback_keyboard.new(action="navigation_calendar", value="")),
#         types.InlineKeyboardButton(text="💁‍♀️Выбрать мастера",
#                                    callback_data=callback_keyboard.new(
#                                        action="choose_specialist_before_change_date", value="")),
#         types.InlineKeyboardButton(text="🔚 В начало",
#                                    callback_data=callback_keyboard.new(action="back", value="")),
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value="")),
#     ]
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
#
#
# def get_set_time():
#     set_time = []
#     if USERS_DATA.get("date") == datetime.datetime.today().date():
#         for slot in SET_TIME:
#             print(SET_TIME)
#             print(slot)
#             if datetime.datetime.now().time() < datetime.time(int(slot.split("_")[0]), int(slot.split("_")[1]), 0):
#                 set_time.append(slot)
#         return set_time
#     else:
#         return SET_TIME
#
#
# def get_keyboard_make_an_appointment(callback_keyboard):
#     buttons = []
#     set_time = get_set_time()
#     for my_time in set_time:
#         time_strip = my_time.replace('_', ":")
#         buttons.append(types.InlineKeyboardButton(
#             text=f"{time_strip}",
#             callback_data=callback_keyboard.new(action="choose_specialist", value=my_time)))
#     buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
#                                               callback_data=callback_keyboard.new(action="back", value="")))
#     buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
#                                               callback_data=callback_keyboard.new(
#                                                   action="back_to_select_date", value="")))
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(*buttons)
#     return keyboard


# def get_keyboard_appointment_have_choose_specialist(callback_keyboard):
#     buttons = []
#     set_time = get_set_time()
#     appointments = Appointments.objects.filter(appointment_date=USERS_DATA["date"], master__pk=USERS_DATA["specialist"])
#     working_time = []
#     for appointment in appointments:
#         working_time.append(appointment.appointment_time.strftime("%H_%M"))
#     for my_time in set_time:
#         if my_time in working_time:
#             continue
#         time_strip = my_time.replace('_', ":")
#         buttons.append(types.InlineKeyboardButton(
#             text=f"{time_strip}",
#             callback_data=callback_keyboard.new(action="personal_data", value=my_time)))
#     buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
#                                               callback_data=callback_keyboard.new(action="back", value="")))
#     buttons.append(types.InlineKeyboardButton(text="🔙 Изменить день",
#                                               callback_data=callback_keyboard.new(
#                                                   action="back_to_select_date", value="")))
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(*buttons)
#     return keyboard


# def get_keyboard_personal_data(callback_keyboard):
#     buttons = [
#         types.InlineKeyboardButton(text="✅ Согласен на обработку ПД",
#                                    callback_data=callback_keyboard.new(action="specify_name", value="")),
#         types.InlineKeyboardButton(text="🔚 В начало",
#                                    callback_data=callback_keyboard.new(action="back", value="")),
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     ]
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(*buttons)
#     return keyboard

# def get_keyboard_recordings(callback_keyboard):
#     user_id = USERS_DATA.get('user_id')
#     client = Client.objects.get(telegram_id=user_id)
#     recordings = Appointments.objects.filter(client=client)[:10]
#     buttons = []
#     for recording in recordings:
#         text = f'{recording.procedure.name}_{recording.appointment_date.strftime("%m-%d")}_{recording.appointment_time}'
#         text_for_value = text.replace(':', '_')
#         buttons.append(
#             types.InlineKeyboardButton(text=f"{text}",
#                                        callback_data=callback_keyboard.new(action="to_recordings", value=f'{text_for_value}')),
#         )
#     buttons.append(types.InlineKeyboardButton(text="🔚 В начало",
#                                               callback_data=callback_keyboard.new(action="back", value="")))
#     buttons.append(
#         types.InlineKeyboardButton(text="☎️Позвонить нам",
#                                    callback_data=callback_keyboard.new(action="call_us", value=""))
#     )
#     keyboard = types.InlineKeyboardMarkup(row_width=2)
#     keyboard.add(*buttons)
#     return keyboard
