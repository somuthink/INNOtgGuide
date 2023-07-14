__all__ = ["bot", "dp", "users_path", "admins_path"]

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import middlewares


from pathlib import Path
import json

from app.data.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

dp.middleware.setup(LoggingMiddleware())


users_path = Path("app/data/users.json")
admins_path = Path("app/data/admins.json")

