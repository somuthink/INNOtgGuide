from aiogram import types

from app.index import *
from app.components.markups import activity_kb, main_menu_callback
from app.components.states import User_States
from app.components.user_class import *
from dataclasses import asdict
import json


@dp.message_handler(commands="start", state="*")
async def _(message: types.Message):
    user_id = message.from_id

    with open(users_path) as f:
        users = json.load(f)

    with open(admins_path) as f:
        admins = json.load(f)

    if str(user_id) not in users:
        # Check if user is admin

        if str(user_id) in admins:
            name = admins[str(user_id)]
            users[str(user_id)] = asdict(USER_CLASS(
                user_id=user_id,
                user_type="ADMIN",
                user_name=name
            ))

            await message.reply(
                text=f'⭐Привет админ⭐ \n__{name}__',
                parse_mode='MarkdownV2'
            )

        else:
            await message.reply(
                text='⭐Привет⭐ \n Я помогу тебе в навигации по университету Инополис'
            )
            await message.answer(
                text='Пожалуйста напиши свое имя чтобы мы могли лучше понимать друг друга)'
            )
            await User_States.enter_name.set()
    else:
        if str(user_id) not in admins:
            name = users[str(user_id)]
            await message.reply(
                text=f'⭐Привет {name["user_name"]}⭐ \n ',

                reply_markup=activity_kb
            )
        else:
            name = users[str(user_id)]
            await message.reply(
                text=f'⭐Привет админ⭐ \n__{name["user_name"]}__'
            )

    with open(users_path, 'w') as f:
        json.dump(users, f)


@dp.message_handler(state=User_States.enter_name)
async def _(message: types.Message):
    user_id = message.from_id
    name = message.text
    with open(users_path) as f:
        users = json.load(f)
    users[str(user_id)] = asdict(USER_CLASS(
        user_id=user_id,
        user_type="Default",
        user_name=name
    ))
    with open(users_path, 'w') as f:
        json.dump(users, f)

    await message.answer(
        text=f"Приятно познакомиться ,__{name}__ \n \nТеперь моежешь выбрать действия ниже \n {' ' * 15}🔽{' ' * 35}🔽",
        parse_mode='MarkdownV2',
        reply_markup=activity_kb
    )


# Обработчик нажатий на кнопки в главном меню
@dp.callback_query_handler(main_menu_callback.filter(choice='nav'), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    # for admin, aid in admins.items():
    #     try:
    #         pass
    #     except Exception as e:
    #         await call.message.answer(str(e))

    await call.message.answer(f"Вы нажали на кнопку ")
