from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from aiogram import Bot


storage = MemoryStorage()
token = os.environ.get("TOKEN")
bot = Bot(token)
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