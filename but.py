from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
import datetime

b0 = KeyboardButton('Записаться на стирку')

b1 = KeyboardButton("Записаться на завтра")
b2 = KeyboardButton("Записаться на сегодня")

b3 = KeyboardButton("Отмена записи")
b4 = KeyboardButton("Список записей на стирку")
b5 = KeyboardButton("Изменить номер комнаты")
b6 = KeyboardButton("Мои записи")

b7 = KeyboardButton('Назад')

b8 = KeyboardButton('Да')
b9 = KeyboardButton('Нет')

b10 = KeyboardButton('Фамилию')
b11 = KeyboardButton('Номер комнаты')
b12 = KeyboardButton('Всё верно')

b13 = KeyboardButton('Аккаунт')
b14 = KeyboardButton("Удалить мой аккаунт")

keyboard_confirm = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_confirm.add(b8).insert(b9)

keyboard_change = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_change.add(b10).insert(b11).add(b12)

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(b0).insert(b3).add(b4).insert(b13).add(b6)

keyboard_record = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_record.add(b1).insert(b2).add(b7)

keyboard_account = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_account.add(b5).insert(b14).add(b7)

i1 = InlineKeyboardButton("19:00-20:00", callback_data="19:00-20:00")
i2 = InlineKeyboardButton("20:00-21:00", callback_data="20:00-21:00")
i3 = InlineKeyboardButton("21:00-22:00", callback_data="21:00-22:00")
i4 = InlineKeyboardButton("22:00-23:00", callback_data="22:00-23:00")
i5 = InlineKeyboardButton("23:00-00:00", callback_data="23:00-23:59")
i6 = InlineKeyboardButton("00:00-01:00", callback_data="23:59-01:00")

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
