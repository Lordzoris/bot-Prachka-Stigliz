import datetime
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
)
from keyboards.but import *

keyboard_confirm = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_confirm.add(b8).insert(b9)

keyboard_change = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_change.add(b10).insert(b11).add(b12)

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(b0).insert(b3).add(b4).insert(b6).add(b13)

keyboard_record = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_record.add(b1).insert(b2).add(b7)

keyboard_account = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_account.add(b5).insert(b14).add(b7)

inline_keyboard_record = InlineKeyboardMarkup(row_width=3).add(i1, i2, i3, i4, i5, i6)


now = datetime.datetime.now()
current_hour = now.hour

if current_hour < 19:
    # кнопки для всех интервалов
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i1, i2, i3, i4, i5, i6)
elif current_hour < 20:
    # кнопки для интервалов с 20 до 01
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i2, i3, i4, i5, i6)
elif current_hour < 21:
    # кнопки для интервалов с 21 до 01
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i3, i4, i5, i6)
elif current_hour < 22:
    # кнопки для интервалов с 22 до 01
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i4, i5, i6)
elif current_hour < 23:
    # кнопки для интервалов с 23 до 01
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i5, i6)
else:
    # кнопка только для интервала с 00 до 01
    inline_keyboard_record_today = InlineKeyboardMarkup(row_width=3).add(i6)
