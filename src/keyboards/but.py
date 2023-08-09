from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

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



i1 = InlineKeyboardButton("19:00-20:00", callback_data="19:00-20:00")
i2 = InlineKeyboardButton("20:00-21:00", callback_data="20:00-21:00")
i3 = InlineKeyboardButton("21:00-22:00", callback_data="21:00-22:00")
i4 = InlineKeyboardButton("22:00-23:00", callback_data="22:00-23:00")
i5 = InlineKeyboardButton("23:00-00:00", callback_data="23:00-23:59")
i6 = InlineKeyboardButton("00:00-01:00", callback_data="23:59-01:00")



