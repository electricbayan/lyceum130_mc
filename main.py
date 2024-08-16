import asyncio
from dotenv import load_dotenv
import logging

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from aiogram import Bot, Dispatcher
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from src.states import PrankState

from config import settings

from aiomcrcon import Client


dp = Dispatcher()


@dp.message(Command('players'))
async def get_players(message: Message):

    async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
        resp = await client.send_cmd('/list')
    resp = resp[0].split(" ")
    players_noun = 'игроков'
    players_count = int(resp[2])
    if players_count == 1:
        players_noun = 'игрок'
    elif 1 < players_count < 5:
        players_noun = 'игрока'

    players = resp[10:]
    response = f'Сейчас на сервере: {players_count} {players_noun}.\n'
    for player in players:
        response += ':- ' + str(player) + '\n'
    await message.answer(response)


@dp.message(Command('prank'))
async def prank_player_getnick(message: Message, state: FSMContext):
    await message.answer('Введите ник')
    await state.set_state(PrankState.nick)

@dp.message(PrankState.nick)
async def prank_player(message: Message, state: FSMContext):
    async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
        resp = await client.send_cmd('/list')
    msg = message.text.strip()
    if msg in resp[0]:
        async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
            resp = await client.send_cmd(f'/title {msg} times 0t 70t 20t')
            await client.send_cmd(f'/title {msg} title "пидор"')
        print(resp)
        await message.answer("Успешно")
    else:
        await message.answer('Такого игрока не существует')
        print(msg)
        print(resp)

    await state.clear()

    


async def main():
    load_dotenv()
    commands = [BotCommand(command="/players", description="Список игроков")]
    bot = Bot(settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())