import asyncio
from dotenv import load_dotenv
import logging

from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandObject


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
async def prank_player_getnick(message: Message, command: CommandObject):
    try:
        args = command.args.split(" ")
    except AttributeError:
        await message.answer('Синтаксис команды: /prank <playername> <text (optional)>')
    if len(args) == 1:
        async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
            resp = await client.send_cmd('/list')
        msg = args[0]
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

    else:
        async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
            resp = await client.send_cmd('/list')
        msg = args[0]
        text = ' '.join(args[1:])
        if msg in resp[0]:
            async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
                resp = await client.send_cmd(f'/title {msg} times 0t 70t 20t')
                await client.send_cmd(f'/title {msg} title "{text}"')
            print(resp)
            await message.answer("Успешно")
        else:
            await message.answer('Такого игрока не существует')
            print(msg)
            print(resp)

@dp.message(Command('tell'))
async def send_message(message: Message, command: CommandObject):
    try:
        args = command.args.split(" ")
        if len(args):
            async with Client(settings.SERVER_IP, settings.SERVER_PORT, settings.SERVER_PASSWORD) as client:
                # print(args)
                text = " ".join(args) + "\n\n@" + message.from_user.first_name
                await client.send_cmd(f'/say {text}')

        else:
            pass
    except AttributeError:
        await message.answer('Синтаксис команды: /tell <text>')


# @dp.message(Command('docs'))
# async
    


async def main():
    load_dotenv()
    commands = [BotCommand(command="/players", description="Список игроков"),
                BotCommand(command="/tell", description="Написать в чат"),
                BotCommand(command='/prank', description="Пранкануть чувачка")]
    bot = Bot(settings.BOT_TOKEN)
    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())