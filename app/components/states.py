__all__ = ["User_States"]

from aiogram.dispatcher.filters.state import State, StatesGroup


class User_States(StatesGroup):
    enter_name = State()
    default = State()
    admin_chatting = State()
