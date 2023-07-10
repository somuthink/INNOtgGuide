from pathlib import Path

from aiogram import types

from app.index import *
from app.components.markups import activity_kb, main_menu_callback
from app.components.states import User_States

import json

from app.user_class import User, UserType



@dp.message_handler(commands="start", state="*")
async def _(message: types.Message):
    user_id = message.from_id


    admin = users.get('admins').get(str(user_id))
    if admin != None:
        await message.reply(
            text=f'⭐Привет админ __{admin}__⭐',
            parse_mode='MarkdownV2',
        )
        await User_States.admin.set()
        return None

    registred = users.get('default').get(str(user_id))
    if registred != None:
        await message.reply(
            text=f'⭐Привет __{registred}__⭐',
            parse_mode='MarkdownV2',
            reply_markup=activity_kb
        )
        await User_States.admin.set()
        return None



    await message.reply(
        text='⭐Привет⭐ \n Я помогу тебе в навигации по университету Инополис'
    )

    await message.answer(
        text='Пожалуйста напиши свое имя чтобы мы могли лучше понимать друг друга)'
    )

    await User_States.enter_name.set()


@dp.message_handler(state=User_States.enter_name)
async def _(message: types.Message):
    await message.answer(
        text=f"Приятно познакомиться ,__{message.text}__ \n \nТеперь моежешь выбрать действия ниже \n {' ' * 15}🔽{' ' * 35}🔽",
        parse_mode='MarkdownV2',
        reply_markup=activity_kb
    )


# Обработчик нажатий на кнопки в главном меню
@dp.callback_query_handler(main_menu_callback.filter(choice='nav'), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    admins = users.get('admins')

    for admin, aid in admins.items():
        try:
            pass
        except Exception as e:
            await call.message.answer(str(e))

    await call.message.answer(f"Вы нажали на кнопку ")
