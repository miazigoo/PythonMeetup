from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.core.management.base import BaseCommand
from django.conf import settings
import asyncio
import logging
from aiogram import Bot, Dispatcher, types

from bot.handlers.add_speaker import register_handlers_add_speakers
from bot.handlers.admin_command import register_handlers_admin
from bot.handlers.common import register_handlers_common
from bot.handlers.fuck_u import register_handlers_fuck_u
from bot.handlers.procedures import register_handlers_procedures
from bot.handlers.speakers import register_handlers_user_speakers
from bot.handlers.users import register_handlers_user

logger = logging.getLogger(__name__)

token = settings.TELEGRAM_BOT_API_KEY
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
admin_id = settings.TELEGRAM_ADMIN_ID
# Диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    # Настройка логирования в stdout
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    # Объявление переменной бота
    # token = settings.TELEGRAM_BOT_API_KEY
    # bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
    # admin_id = settings.TELEGRAM_ADMIN_ID
    # # Диспетчер
    # dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_common(dp, admin_id)
    register_handlers_procedures(dp)
    register_handlers_admin(dp)
    register_handlers_user(dp)
    register_handlers_fuck_u(dp)
    register_handlers_add_speakers(dp)
    register_handlers_user_speakers(dp)

    # Запуск поллинга

    await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.start_polling()


# Название класса
class BotCommand(BaseCommand):
    # Используется как описание команды обычно
    help = 'Implemented to Django application telegram bot setup command'

    # Запуск бота
    asyncio.run(main())
