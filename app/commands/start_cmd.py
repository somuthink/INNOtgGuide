from aiogram import types

from app.index import *
from app.components.states import User_States
from app.components.user_class import *
from dataclasses import asdict
import json


@dp.message_handler(commands="start", state="*")
async def _(message: types.Message):
    async def greet_new_user():
        await message.reply(
            text="⭐Привет⭐ \n Я помогу тебе в навигации по университету Инополис"
        )
        await message.answer(
            text="Пожалуйста напиши свое имя чтобы мы могли лучше понимать друг друга)"
        )
        await User_States.enter_name.set()

    async def greet_admin(name):
        await message.reply(
            text=f"⭐Привет админ⭐ \n__{name}__",
        )

    async def greet_existing_user(name):
        await message.reply(
            text=f"⭐Привет __{name}__⭐ \n Пиши /main чтобы воспользоваться главным меню",
            parse_mode="MarkdownV2",
        )

    user_id = message.from_id

    users = get_users()

    with open(admins_path) as f:
        admins = json.load(f)

    # isn't logged
    if str(user_id) not in users:
        # admin
        if str(user_id) in admins:
            name = admins[str(user_id)]["user_name"]
            users[str(user_id)] = asdict(
                USER_CLASS(user_id=user_id, user_type="ADMIN", user_name=name)
            )
            await greet_admin(name)
        # default
        else:
            await greet_new_user()

    # isn logged
    else:
        # admin
        if str(user_id) not in admins:
            name = users[str(user_id)]["user_name"]
            await greet_existing_user(name)
        # default
        else:
            name = users[str(user_id)]["user_name"]
            await greet_admin(name)

    with open(users_path, "w") as f:
        json.dump(users, f)
