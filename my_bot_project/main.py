from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor

from data import config  # config.py должен содержать BOT_TOKEN
from loader import dp, bot  # где инициализированы dp и bot
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify

import middlewares, filters, handlers
from utils.db_api.userdb import UserDatabase
from utils.db_api.kino_db import KinoDatabase
from utils.db_api.postgresql import Database

# Создаем экземпляры баз
user_db = UserDatabase()
kinodb = KinoDatabase()
db = Database()

# Функция запуска
async def on_startup(dispatcher: Dispatcher):
    await user_db.create_table_users()
    await kinodb.create_table_kino()
    await db.create()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    print("🤖 Bot ishga tushdi!")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
