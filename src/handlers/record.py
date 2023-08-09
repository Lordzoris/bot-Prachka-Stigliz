import datetime
import sys
import logging
from aiogram.bot import bot
from handlers.state import Reg, dp
from aiogram import types
sys.path.append('..')
from db.databaseconnect import check_record_user, add_record_tomorrow, add_record_today, delete_record
from keyboards.keyboards import keyboard_record, keyboard_main, inline_keyboard_record, inline_keyboard_record_today


@dp.message_handler(state=Reg.record, text='Записаться на стирку')
async def choose_record(message: types.Message):
    await message.answer("Выберите день записи:", reply_markup=keyboard_record)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text='Назад')
async def returns(message: types.Message):
    await message.answer('Назад в меню', reply_markup=keyboard_main)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Записаться на завтра")
async def get_record(message: types.Message):
    now_full = datetime.datetime.now()
    hour = now_full.hour
    if hour < 21:
        await message.answer("Сейчас записаться на стирку нельзя. Запись начинается с 21:00")
    else:
        res = await check_record_user(message.from_user.id)
        if not res:
            await Reg.record_tomorrow.set()
            await message.answer("Выберите время записи на завтра:", reply_markup=inline_keyboard_record)
        else:
            await message.answer("Вы уже записаны на стирку, записаться можно только на один временной слот.")


@dp.callback_query_handler(state=Reg.record_tomorrow)
async def process_callback_tomorrow(callback_query: types.CallbackQuery):
    res = await add_record_tomorrow(callback_query.data, callback_query.from_user.id)
    await Reg.record.set()
    logging.info(f"res = {res}")
    if res == 0:
        await callback_query.message.answer("Мест на стирку на это время больше нет.")
    elif res == 1:
        await callback_query.message.answer("Вы записались на стирку!")
    else:
        await callback_query.message.answer(
            "Вы уже записаны на стирку, записаться можно только на один временной слот."
        )
    await Reg.record.set()


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Записаться на сегодня")
async def get_record_today(message: types.Message):
    await Reg.record_today.set()
    await message.answer("Выберите время записи на сегодня:", reply_markup=inline_keyboard_record_today)


@dp.callback_query_handler(state=Reg.record_today)
async def process_callback_today(callback_query: types.CallbackQuery):
    res = await add_record_today(callback_query.data, callback_query.from_user.id)
    await Reg.record.set()
    logging.info(f"res = {res}")
    if res == 0:
        await callback_query.message.answer("Мест на стирку на это время больше нет.")
    elif res == 1:
        await callback_query.message.answer("Вы записались на стирку!")
    else:
        await callback_query.message.answer(
            "Вы уже записаны на стирку, записаться можно только на один временной слот."
        )


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Отмена записи")
async def del_record(message: types.Message):
    await delete_record(message.from_user.id)
    await message.answer("Запись отменена!")