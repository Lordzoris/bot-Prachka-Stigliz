import os
import sys
import logging
from states.state import Reg, dp
sys.path.append('..')
from db.databaseconnect import reg_connect, reg_test
from keyboards.keyboards import keyboard_main, keyboard_confirm, keyboard_change
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    a = types.ReplyKeyboardRemove()
    if await reg_test(message.from_user.id):
        await message.answer("Привет!", reply_markup=keyboard_main)
        await Reg.record.set()
    else:
        logging.info(f"{os.getcwd()}")
        with open("./src/replicas/hello.txt", "r", encoding="UTF-8") as f:
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
