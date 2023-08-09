from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import databaseconnect
import datetime
import asyncio


async def cleaning_db():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        databaseconnect.delete_old_record,
        trigger='cron',
        hour="00",
        start_date=datetime.datetime.now(),
    )
    scheduler.start()