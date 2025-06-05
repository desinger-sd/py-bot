from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.userdb import UserDatabase
from utils.db_api.kino_db import KinoDatabase
from utils.db_api.postgresql import Database


from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

user_db= UserDatabase()
kinodb=KinoDatabase()
db=Database()
