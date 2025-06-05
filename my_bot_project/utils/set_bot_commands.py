from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("help", "Yordam"),
            types.BotCommand("count", "Foydalanuvchilar sonini ko‘rish"),
            types.BotCommand("reklama", "Avtomatik reklama yuborishni boshlash"),
            types.BotCommand("stop_reklama", "Avtomatik reklamani to‘xtatish"),
        ]
    )
