from aiogram import executor

import app.commands.cmds  # noqa
from app.index import dp

if __name__ == "__main__":
    executor.start_polling(dispatcher=dp, skip_updates=True)
