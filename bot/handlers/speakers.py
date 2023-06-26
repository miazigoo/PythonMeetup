from contextlib import suppress

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import MessageNotModified
from asgiref.sync import sync_to_async

from bot.keyboard.keyboard_speaker import get_keyboard_back_and_next_question
from bot.keyboard.keyboard_user import get_keyboard_back
from bot.models import Speaker, Flag, Client, Question

callback_keyboard = CallbackData("procedures", "action", "value", "info")
user_data = {}


async def update_text(message: types.Message, answer_text, get_keyboard):
    with suppress(MessageNotModified):
        await message.edit_text(answer_text,
                                reply_markup=get_keyboard(callback_keyboard), parse_mode="MarkdownV2")


@sync_to_async()
def add_speakers_flag(telegram_id):
    client = Client.objects.get(
        telegram_id=telegram_id
    )
    speaker = Speaker.objects.get(client=client)
    flag, create = Flag.objects.get_or_create(speaker=speaker)
    if create:
        flag = Flag.objects.get(speaker=speaker)
    return flag, speaker


@sync_to_async()
def get_first_question(speaker):
    question = Question.objects.filter(speaker=speaker)
    return question


async def speakers_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    action = callback_data["action"]
    telegram_id = call.from_user.id
    flag, speaker = await add_speakers_flag(telegram_id)
    question = await get_first_question(speaker)
    len_question = len(question)
    if action == "start_performance":
        flag.flag = True
        flag.save()
        text = '✅ Вы *начали* выступление'
        await update_text(call.message, text, get_keyboard_back)
    elif action == "end_performance":
        flag.flag = False
        flag.save()
        text = '✅ Вы *закончили* выступление'
        question.delete()
        await update_text(call.message, text, get_keyboard_back)
    elif action == "read_questions":
        user_data['telegram_id'] = 1
        print('question.count = ', len_question)
        if question:
            text = f'Всего вопросов: {len_question} \nВопрос от *{question[0].nikname}* \n{question[0].text}'
            keyboard = get_keyboard_back
            if len_question > 1:
                keyboard = get_keyboard_back_and_next_question
            await update_text(call.message, text, keyboard)
        else:
            text = 'Вопросов пока нет'
        await update_text(call.message, text, get_keyboard_back)

    await call.answer()


async def next_question(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    telegram_id = call.from_user.id
    flag, speaker = await add_speakers_flag(telegram_id)
    numb_value = user_data.get('telegram_id', 1)
    if action == "next_question":
        user_data['telegram_id'] = numb_value + 1
        question = await get_first_question(speaker)
        len_question = len(question)

        keyboard = get_keyboard_back_and_next_question
        text = f'Вопрос{numb_value+1} \nВопрос от *{question[numb_value].nikname}*\n\n{question[numb_value].text}'
        if (numb_value+1) == len_question:
            text = f'*Последний вопрос*\nВопрос от *{question[numb_value].nikname}*\n\n{question[numb_value].text}'
            keyboard = get_keyboard_back

        await update_text(call.message, text, keyboard)


def register_handlers_user_speakers(dp: Dispatcher):
    # dp.register_message_handler(send_question, state=PersonalData.waiting_ask_question)
    # dp.register_message_handler(make_newsletter_for_speakers, state=PersonalData.waiting_make_newsletter_for_speakers)

    dp.register_callback_query_handler(
        speakers_callback,
        callback_keyboard.filter(action=[
            "start_performance",
            "end_performance",
            "read_questions",
        ]),
        state="*", )
    dp.register_callback_query_handler(
        next_question,
        callback_keyboard.filter(action=[
            "next_question",
        ]),
        state="*", )
