__all__ = ["activity_kb", "main_menu_callback"]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData

main_menu_callback = CallbackData("menu",  # Префикс
                                  "choice"  # Имя параметра
                                  )

activity_kb = InlineKeyboardMarkup()

map = InlineKeyboardButton("Карта", callback_data=main_menu_callback.new(choice="nav"))
helpers = InlineKeyboardButton("Вожатые", callback_data=main_menu_callback.new(choice="call"))

activity_kb.add(map, helpers)