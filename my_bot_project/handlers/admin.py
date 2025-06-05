from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp, user_db, bot
import asyncio

# FSM состояния для рассылки
class ReklamaState(StatesGroup):
    waiting_for_content = State()
    waiting_for_interval = State()

# Хранилище состояния рассылки
broadcast_data = {
    "photo": None,
    "caption": None,
    "interval": None,
    "task": None,
}

# Команда для подсчёта пользователей
@dp.message_handler(commands="count")
async def count_users(message: types.Message):
    count = await user_db.count_users()
    await message.answer(f"Foydalanuvchilar soni: {count} ta")

# Команда для запуска рассылки
@dp.message_handler(Command("reklama"))
async def start_reklama(message: types.Message):
    await message.answer("📸 Iltimos, sarlavhasi bilan rasm yuboring.")
    await ReklamaState.waiting_for_content.set()

# Обработка фото и подписи
@dp.message_handler(content_types=types.ContentType.PHOTO, state=ReklamaState.waiting_for_content)
async def handle_reklama_content(message: types.Message, state: FSMContext):
    broadcast_data["photo"] = message.photo[-1].file_id
    broadcast_data["caption"] = message.caption or "📢 Реклама"
    await message.answer("⏰ Necha daqiqada bir yuborilsin? Masalan: 10")
    await ReklamaState.waiting_for_interval.set()

# Установка интервала и запуск рассылки
@dp.message_handler(state=ReklamaState.waiting_for_interval)
async def set_interval_and_start(message: types.Message, state: FSMContext):
    try:
        interval = int(message.text)
        broadcast_data["interval"] = interval
    except ValueError:
        return await message.answer("❗️ Iltimos, butun son kiriting (necha daqiqa)")

    if broadcast_data["task"] is not None:
        broadcast_data["task"].cancel()

    loop = asyncio.get_event_loop()
    broadcast_data["task"] = loop.create_task(auto_broadcast())

    await message.answer(f"✅ Har {interval} daqiqada avtomatik reklama yuboriladi.")
    await state.finish()

# Фоновая задача для рассылки
async def auto_broadcast():
    print("[ℹ️] Avtomatik reklama yuborish boshlandi.")
    while True:
        users = await user_db.select_all_users()
        for user in users:
            try:
                await bot.send_photo(
                    chat_id=int(user['telegram_id']),
                    photo=broadcast_data["photo"],
                    caption=broadcast_data["caption"]
                )
            except Exception as e:
                print(f"[❌] Xatolik {user}: {e}")
        await asyncio.sleep(broadcast_data["interval"] * 60)

# Команда для остановки рассылки
@dp.message_handler(Command("stop_reklama"))
async def stop_reklama(message: types.Message):
    task = broadcast_data.get("task")
    if task and not task.done():
        task.cancel()
        broadcast_data["task"] = None
        await message.answer("🛑 Avtomatik reklama to‘xtatildi.")
    else:
        await message.answer("🚫 Faol reklama topilmadi.")
