import asyncio
import os

import databaseconnect
from databaseconnect import *
from but import keyboard1, keyboard2, inline_keyboard1, inline_keyboard2
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage = MemoryStorage()
token = "6121456100:AAHe-3UOoakDUqvckJejyXBzK8NV5zOESdg"
bot = Bot(token)  # =os.environ["TOKEN"])
dp = Dispatcher(bot, storage=storage)


class Reg(StatesGroup):
    name = State()
    room = State()
    record = State()
    changes = State()
    record_tomorrow = State()
    record_today = State()


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    a = types.ReplyKeyboardRemove()
    if await reg_test(message.from_user.id):
        await message.answer("Привет!", reply_markup=keyboard1)
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
        await message.answer("Отлично, регистрация завершена!", reply_markup=keyboard1)
        await Reg.next()

@dp.message_handler(state=Reg.record, text='Записаться на стирку')
async def choose_record(message: types.Message):
    await message.answer("Выберите день записи:", reply_markup=keyboard2)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text='Назад')
async def returns(message: types.Message):
    await message.answer("Назад", reply_markup=keyboard1)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Записаться на завтра")
async def get_record(message: types.Message):
    now_full = datetime.datetime.now()
    hour = now_full.hour
    if hour < 21:
        await message.answer("Сейчас записаться на стирку нельзя. Запись начинается с 21:00")
    else:
        await Reg.record_tomorrow.set()
        await message.answer("Выберите время записи на завтра:", reply_markup=inline_keyboard1)


@dp.callback_query_handler(state=Reg.record_tomorrow)
async def process_callback_tomorrow(callback_query: types.CallbackQuery):
    res = await add_record_tomorrow(callback_query.data, callback_query.from_user.id)
    await Reg.record.set()
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
    await Reg.record.set()


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Записаться на сегодня")
async def get_record_today(message: types.Message):
    await Reg.record_today.set()
    await message.answer("Выберите время записи на сегодня:", reply_markup=inline_keyboard2)


@dp.callback_query_handler(state=Reg.record_today)
async def process_callback_today(callback_query: types.CallbackQuery):
    res = await add_record_today(callback_query.data, callback_query.from_user.id)
    await Reg.record.set()
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


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Мои записи")
async def check_record(
        message: types.Message,
):
    res = await check_record_user(message.from_user.id)
    if not res:
        await message.answer("Запись на стирку не найдена.")
    else:
        await message.answer("Вы записаны на стирку на следующее время:\n" + str(res))


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Отмена записи")
async def del_record(
        message: types.Message,
):
    await delete_record(message.from_user.id)
    await message.answer("Запись отменена!")


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Список записей на стирку")
async def lists_wash(message: types.Message):
    lists = await list_wash()
    await message.answer("Список на стирку: \n" + lists)


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
    await change_number(message.from_user.id, data["number"])
    await message.answer("Номер комнаты изменён!")
    await Reg.record.set()


async def cleaning_db():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        databaseconnect.delete_old_record,
        trigger='cron',
        hour="00",
        start_date=datetime.datetime.now(),
    )
    scheduler.start()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cleaning_db())
    executor.start_polling(dp)
