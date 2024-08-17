import asyncio
from dotenv import load_dotenv
import logging

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher

from src.routers.main_rt import main_rt
from config import settings


async def main():
    load_dotenv()
    dp = Dispatcher()
    dp.include_router(main_rt)
    commands = [BotCommand(command="/players", description="Список игроков"),
                BotCommand(command="/tell", description="Написать в чат"),
                BotCommand(command='/prank', description="Пранкануть чувачка")]
    bot = Bot(settings.BOT_TOKEN)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())