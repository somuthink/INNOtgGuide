__all__ = ["activity_kb", "campus_kb", "admin_chat_kb", "places_kb", "main_menu_callback", "campuses_callback",
           "places_callback"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

from app.data.navigations import *

main_menu_callback = CallbackData("menu", "choice")  # Префикс  # Имя параметра

campuses_callback = CallbackData("campuses", "choice")

places_callback = CallbackData("places", "choice")

activity_kb = InlineKeyboardMarkup()

admin_chat_kb = InlineKeyboardMarkup()

campus_kb = InlineKeyboardMarkup()

places_kb = InlineKeyboardMarkup()

campus_select = InlineKeyboardButton(
    "Выбрать кампус🏢", callback_data=main_menu_callback.new(choice="campus")
)
map = InlineKeyboardButton(
    "Навигатор🗺", callback_data=main_menu_callback.new(choice="nav")
)
helpers = InlineKeyboardButton(
    "Вожатые👾", callback_data=main_menu_callback.new(choice="call")
)

leave_admin_chat = InlineKeyboardButton(
    "Покинуть чат🦶", callback_data=main_menu_callback.new(choice="leave")
)

zero = InlineKeyboardButton("Универ 🟩", callback_data=campuses_callback.new(choice="0 🟩"))
first = InlineKeyboardButton("1 🟩", callback_data=campuses_callback.new(choice="1 🟩"))
second = InlineKeyboardButton("2 🟧", callback_data=campuses_callback.new(choice="2 🟧"))
third = InlineKeyboardButton("3 🟪", callback_data=campuses_callback.new(choice="3 🟪"))
fourth = InlineKeyboardButton("4 🟩", callback_data=campuses_callback.new(choice="4 🟩"))

places = [
    InlineKeyboardButton(text=place,
                         callback_data=places_callback.new(choice=place))
    for place in navigations]

places_kb.add(*places)
activity_kb.add(campus_select, map, helpers)
admin_chat_kb.add(leave_admin_chat)
campus_kb.add(zero, first, second, third, fourth)
