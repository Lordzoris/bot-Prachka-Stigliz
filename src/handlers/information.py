import sys
from states.state import Reg, dp
from aiogram import types
sys.path.append('..')
from db.databaseconnect import check_record_user, list_wash


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Мои записи")
async def check_record(message: types.Message):
    res = await check_record_user(message.from_user.id)
    if not res:
        await message.answer("Запись на стирку не найдена.")
    else:
        await message.answer("Вы записаны на стирку на следующее время:\n" + str(res))


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Список записей на стирку")
async def lists_wash(message: types.Message):
    lists = await list_wash()
    await message.answer("Список на стирку: \n" + lists)