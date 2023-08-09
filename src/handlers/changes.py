import sys
from states.state import Reg, dp
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
sys.path.append('..')
from db.databaseconnect import change_room


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Изменить номер комнаты")
async def changes_number(message: types.Message):
    await message.answer("Введите новый номер комнаты:")
    await Reg.changes.set()


@dp.message_handler(state=Reg.changes)
async def changes_number_room(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["number"] = message.text
        if not message.text.isdigit():
            await message.answer("Номер комнаты должен состоять из цифр")
            return
    await change_room(message.from_user.id, data["number"])
    await message.answer("Номер комнаты изменён!")
    await Reg.record.set()

