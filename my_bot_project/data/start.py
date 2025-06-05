import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import dp,user_db,bot
import asyncpg


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):

    telegram_id=message.from_user.id
    username=message.from_user.username
    try:
        await user_db.add_user(
            telegram_id=telegram_id,
            username=username
        )

    except asyncpg.exceptions.UniqueViolationError:
        user=await user_db.select_user(telegram_id=telegram_id)

    await message.answer("👋 Assalomu alaykum xush kelibsiz botimizga")

    #Adminga xabar beramiz
    await bot.send_message(
        chat_id=ADMINS[0],
        text=f"Foydalanuvchi qushildi @{user_db[2]}"
    )




