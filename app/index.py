__all__ = ["bot", "dp", "users"]

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from pathlib import Path
import json

from app.data.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

path = Path("data/users.json")

with open(path) as f:   users = json.load(f)
