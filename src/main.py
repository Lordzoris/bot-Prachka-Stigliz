import asyncio
import os

from db.clear_db import cleaning_db
from db.databaseconnect import *
from handlers.account import *
from handlers.changes import *
from handlers.information import *
from handlers.record import *
from handlers.registration import *
from handlers.state import *
from keyboards.but import *
from keyboards.keyboards import *
from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging





if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(cleaning_db())
    executor.start_polling(dp)
