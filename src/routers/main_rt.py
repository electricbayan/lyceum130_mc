from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from config import settings
from aiomcrcon import Client


main_rt: Router = Router()


@main_rt.message(Command('players'))
async def get_players(message: Message):

    async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
        resp = await client.send_cmd('/list')
    resp = resp[0].split(" ")
    players_noun = 'игроков'
    players_count = int(resp[2])
    if players_count == 1:
        players_noun = 'игрок'
    elif 2 <= players_count <= 4:
        players_noun = 'игрока'

    players = resp[10:]
    await message.answer(f'Сейчас на сервере: {players_count} {players_noun}.')