import asyncio
import os

import databaseconnect
from databaseconnect import *
from but import keyboard_main, keyboard_record, inline_keyboard_record, inline_keyboard_record_today, keyboard_confirm, keyboard_change, keyboard_account
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

storage = MemoryStorage()
token = ""
bot = Bot(token)  # =os.environ["TOKEN"])
dp = Dispatcher(bot, storage=storage)


class Reg(StatesGroup):
    name = State()
    room = State()
    confirm = State()
    change_reg = State()
    change_name = State()
    change_number = State()
    record = State()
    changes = State()
    record_tomorrow = State()
    record_today = State()
    deleted = State()


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    a = types.ReplyKeyboardRemove()
    if await reg_test(message.from_user.id):
        await message.answer("Привет!", reply_markup=keyboard_main)
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
        data["number"] = message.text
        await Reg.confirm.set()
        await message.answer(
            f"Вы ввели:\nФамилия: {data['name']}\nНомер комнаты: {data['number']}\nВсё верно?",
            reply_markup=keyboard_confirm)


@dp.message_handler(state=Reg.confirm)
async def confirm_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == "да":
            await reg_connect(message.from_user.id, data["name"], data["number"])
            await message.answer("Отлично, регистрация завершена!", reply_markup=keyboard_main)
            await Reg.record.set()
        elif message.text.lower() == "нет":
            await message.answer("Что нужно исправить?", reply_markup=keyboard_change)
            await Reg.change_reg.set()


@dp.message_handler(state=Reg.change_reg, text="Фамилию")
async def change_name(message: types.Message):
    await message.answer("Введите свою фамилию:")
    await Reg.change_name.set()


@dp.message_handler(state=Reg.change_name)
async def confirm_name(message: types.Message, state: FSMContext):
    if not message.text.isalpha():
        await message.answer("Фамилия должна состоять из букв")
        return
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer(
        f"Вы ввели:\nФамилия: {data['name']}\nНомер комнаты: {data['number']}\nВсё верно?",
        reply_markup=keyboard_confirm)
    await Reg.confirm.set()


@dp.message_handler(state=Reg.change_reg, text="Номер комнаты")
async def change_number(message: types.Message):
    await message.answer("Введите номер комнаты:")
    await Reg.change_number.set()


@dp.message_handler(state=Reg.change_number)
async def confirm_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if not message.text.isnumeric():
            await message.answer("Номер комнаты должен состоять из цифр")
            return
        data['number'] = message.text
    await message.answer(
        f"Вы ввели:\nФамилия: {data['name']}\nНомер комнаты: {data['number']}\nВсё верно?",
        reply_markup=keyboard_confirm)
    await Reg.confirm.set()

@dp.message_handler(state=Reg.change_reg, text="Всё верно")
async def confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Отлично, регистрация завершена!", reply_markup=keyboard_main)
        await reg_connect(message.from_user.id, data["name"], data["number"])
        await state.reset_state()
        await Reg.record.set()

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
    await message.answer("Выберите время записи на сегодня:", reply_markup=inline_keyboard_record_today)


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
async def check_record(message: types.Message):
    res = await check_record_user(message.from_user.id)
    if not res:
        await message.answer("Запись на стирку не найдена.")
    else:
        await message.answer("Вы записаны на стирку на следующее время:\n" + str(res))


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Отмена записи")
async def del_record(message: types.Message):
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
    await change_room(message.from_user.id, data["number"])
    await message.answer("Номер комнаты изменён!")
    await Reg.record.set()


@dp.message_handler(state=Reg.record, text='Аккаунт')
async def choose_record(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=keyboard_account)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Удалить мой аккаунт")
async def delete_accounts(message: types.Message):
    await delete_account(message.from_user.id)
    await Reg.deleted.set()
    await message.answer("Ваш аккаунт удалён!", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Reg.deleted)
async def for_deleted(message: types.Message):
    await message.answer("Ваш аккаунт был удален. Для продолжения работы с ботом, пожалуйста, создайте новый аккаунт.\nЧтобы создать новый аккаунт нажмите /start")
    return


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
