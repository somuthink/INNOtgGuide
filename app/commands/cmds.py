import aiogram.utils.exceptions
from aiogram import types

from app.index import *
from app.components.markups import *
from app.components.states import User_States
from app.components.user_class import *
from dataclasses import asdict
import json
from math_problem_generator import generator

from app.data.navigations import *

def get_users():
    with open(users_path) as f:
        return json.load(f)


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
            parse_mode="MarkdownV2"
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
            name = admins[str(user_id)]
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


@dp.message_handler(commands="main", state="*")
async def _(message: types.Message):
    await User_States.default.set()
    user_id = message.from_id
    users = get_users()
    user = users[str(user_id)]
    name = user["user_name"]
    campus = user["user_campus"]

    if user["user_type"] == "Default":
        await message.answer(
            text=f"__{name}__ ты находишься в кампусе {campus}",
            parse_mode="MarkdownV2",
            reply_markup=activity_kb,
        )
    else:
        await message.answer(
            text=f"АДМИН",
            parse_mode="MarkdownV2",
        )


@dp.message_handler(state=User_States.enter_name)
async def _(message: types.Message):
    user_id = message.from_id
    name = message.text
    users = get_users()
    users[str(user_id)] = asdict(
        USER_CLASS(user_id=user_id, user_type="Default", user_name=name)
    )
    with open(users_path, "w") as f:
        json.dump(users, f)

    await message.answer(
        text=f"Приятно познакомиться ,__{name}__ \n \nТеперь пожалйста выбери свой кампус",
        parse_mode="MarkdownV2",
        reply_markup=campus_kb,
    )

    await User_States.default.set()


@dp.message_handler(state=User_States.admin_chatting)
async def _(message: types.Message):
    user_id = message.from_id

    users = get_users()
    name = users[str(user_id)]["user_name"]
    campus = users[str(user_id)]["user_campus"]
    answer = users[str(user_id)]["user_correct_answer"]

    text = message.text

    text_words = text.split()

    user_answer = int(text_words[0])
    user_text = ' '.join(text_words[1:])

    if int(user_answer) == int(answer):

        with open(admins_path) as f:
            admins = json.load(f)
        for admin in admins:
            try:
                await bot.send_message(admin, text=f"Кампус {campus} - {name} \n{user_text}")
            except Exception as e:
                await message.answer(text=str(e))
        math_problem = generator.simple_problems(
            "add", no_of_problems=1, min_number=1, max_number=10, numbers=3
        )[0]
        question = " + ".join(map(str, math_problem["numbers"]))

        users[str(user_id)]["user_correct_answer"] = math_problem["solution"]
        with open(users_path, "w") as f:
            json.dump(users, f)

        await message.answer(
            text=f"Сообщение отправленно\n Для отправки следущего сообщения реши новый пример\n`{question} = ''`",
            parse_mode="MarkdownV2",
            reply_markup=admin_chat_kb
        )

    else:
        await message.answer(
            text=f"Ответ не верный,чат остановлен\nПиши /main чтобы воспользоваться главным меню",
            parse_mode="MarkdownV2",
        )
        await User_States.default.set()


@dp.callback_query_handler(campuses_callback.filter(), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    users = get_users()
    users[str(user_id)]["user_campus"] = callback_data["choice"]
    with open(users_path, "w") as f:
        json.dump(users, f)

    text = f"Ваш кампус теперь {callback_data['choice']} \n Пиши /main чтобы воспользоваться главным меню"
    try:
        await call.message.edit_text(text, reply_markup=campus_kb)
    except aiogram.utils.exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(main_menu_callback.filter(choice="campus"), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    try:
        await call.message.edit_text(text=f"Выбирай кампус в котором сейчас находишься",
                                     parse_mode="MarkdownV2",
                                     reply_markup=campus_kb, )
    except aiogram.utils.exceptions.MessageNotModified:
        pass
    # await call.message.answer(
    #     text=f"Выбирай кампус в котором сейчас находишься",
    #     parse_mode="MarkdownV2",
    #     reply_markup=campus_kb,
    # )


@dp.callback_query_handler(main_menu_callback.filter(choice="leave"), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    await User_States.default.set()
    await call.message.answer(
        text=f"Чат покинут\nПиши /main чтобы воспользоваться главным меню",
        parse_mode="MarkdownV2",
    )


@dp.callback_query_handler(main_menu_callback.filter(choice="nav"), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    try:
        await call.message.edit_text(f"Выбери место путь до которого хочешь узнать ", reply_markup=places_kb)
    except aiogram.utils.exceptions.MessageNotModified:
        pass


@dp.callback_query_handler(main_menu_callback.filter(choice="call"), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id

    users = get_users()

    math_problem = generator.simple_problems(
        "add", no_of_problems=1, min_number=1, max_number=10, numbers=3
    )[0]
    question = " + ".join(map(str, math_problem["numbers"]))

    try:
        await call.message.edit_text(
            f"Напиши сообщение вожатым чтобы они тебе помогли\n \nНо сначал реши пример \(это нужно для защиты от спама\) \n`{question} = ''`\nответ запиши цифрами перед своим сообщением \n \n Пример: \n 27 Помогите найти кулер",
            parse_mode="MarkdownV2")
    except aiogram.utils.exceptions.MessageNotModified:
        pass

    # await call.message.answer(
    #     f"Напиши сообщение вожатым чтобы они тебе помогли\n \nНо сначал реши пример \(это нужно для защиты от спама\) \n`{question} = ''`\nответ запиши цифрами перед своим сообщением \n \n Пример: \n 27 Помогите найти кулер",
    #     parse_mode="MarkdownV2"
    # )

    users[str(user_id)]["user_correct_answer"] = math_problem["solution"]
    with open(users_path, "w") as f:
        json.dump(users, f)

    await User_States.admin_chatting.set()


@dp.callback_query_handler(places_callback.filter(), state="*")
async def _(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id

    users = get_users()

    user_campus = users[str(user_id)]["user_campus"]

    place = callback_data["choice"]




    await call.message.answer(text = f"{navigations[place]}")
