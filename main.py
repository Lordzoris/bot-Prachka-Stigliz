import asyncio
import os

import databaseconnect
from databaseconnect import *
from but import keybrd, inlinekb1
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage = MemoryStorage()
bot = Bot(token)  # =os.environ["TOKEN"])
dp = Dispatcher(bot, storage=storage)


class Reg(StatesGroup):
    name = State()
    room = State()
    record = State()


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    a = types.ReplyKeyboardRemove()
    if await reg_test(message.from_user.id):
        await message.answer("Привет!", reply_markup=keybrd)
        await Reg.record.set()
    else:
        with open("replicas/hello.txt", "r", encoding="UTF-8") as f:
            await message.answer(f.read(), reply_markup=a)
        await Reg.name.set()


@dp.message_handler(state=Reg.name)
async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isalpha():
            await message.answer("Фамилия должна состоять из букв")
            return
        data["name"] = message.text
    await Reg.next()
    await message.answer("Укажите номер своей комнаты:")


@dp.message_handler(state=Reg.room)
async def get_room(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isnumeric():
            await message.answer("Номер комнаты должен состоять из цифр")
            return

        await reg_connect(message.from_user.id, data["name"], message.text)
        await message.answer("Отлично, регистрация завершена!", reply_markup=keybrd)
        await Reg.next()


@dp.message_handler(state=Reg.record, text="Записаться на стирку")
async def get_record(
    message: types.Message,
):
    await message.answer("Выберите время записи:", reply_markup=inlinekb1)


@dp.callback_query_handler(state=Reg.record)
async def process_callback(callback_query: types.CallbackQuery):
    res = await add_record(callback_query.data, callback_query.from_user.id)
    if res == 0:
        await bot.send_message(
            callback_query.from_user.id, f"Мест на стирку на это время больше нет."
        )
    elif res == 1:
        await bot.send_message(callback_query.from_user.id, f"Вы записались на стирку!")
    else:
        await bot.send_message(
            callback_query.from_user.id,
            f"Вы уже записаны на стирку, записаться можно только на один временной слот.",
        )


@dp.message_handler(state=Reg.record, text="Мои записи")
async def check_record(
    message: types.Message,
):
    res = await check_record_user(message.from_user.id)
    if not res:
        await message.answer("Запись на стирку не найдена.")
    else:
        await message.answer("Вы записаны на стирку на следующее время:\n" + str(res))


@dp.message_handler(state=Reg.record, text="Отмена записи")
async def del_record(
    message: types.Message,
):
    await delete_record(message.from_user.id)
    await message.answer("Запись отменена!")


@dp.message_handler(state=Reg.record, text="Список на стирку")
async def lists_wash(message: types.Message):
    lists = await list_wash()
    await message.answer("Список на стирку: \n" + lists)


async def cleaning_db():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        databaseconnect.delete_old_record,
        trigger='cron',
        #trigger="interval", проверка работы
        #seconds=1,
        hour="00",
        start_date=datetime.datetime.now(),
    )
    scheduler.start()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cleaning_db())
    executor.start_polling(dp)
