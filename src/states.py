from aiogram.fsm.state import State, StatesGroup


class PrankState(StatesGroup):
    nick = State()
    