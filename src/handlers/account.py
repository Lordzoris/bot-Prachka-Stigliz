import sys
from states.state import Reg, dp
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

sys.path.append('..')
from db.databaseconnect import delete_account
from keyboards.keyboards import keyboard_account


@dp.message_handler(state=Reg.record, text='Аккаунт')
async def choose_record(message: types.Message):
    await message.answer("Выберите действие:", reply_markup=keyboard_account)


@dp.message_handler(state=[Reg.record, Reg.record_tomorrow, Reg.record_today], text="Удалить мой аккаунт")
async def delete_accounts(message: types.Message):
    await delete_account(message.from_user.id)
    await Reg.deleted.set()
    await message.answer("Ваш аккаунт удалён!", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Reg.deleted)
async def for_deleted(message: types.Message, state: FSMContext):
    await message.answer(
        "Ваш аккаунт был удален. Для продолжения работы с ботом, пожалуйста, создайте новый аккаунт.\nЧтобы создать новый аккаунт нажмите /start")
    await state.finish()
    return
