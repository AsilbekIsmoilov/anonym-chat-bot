from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from storage.redis import redis
from services.matcher import start_search, stop_chat

router = Router()

chat_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏭ Keyingi"), KeyboardButton(text="⛔ To‘xtatish")]
    ],
    resize_keyboard=True
)


# 1️⃣ Chatni boshlash
@router.message(F.text == "💬 Chatni boshlash")
async def start_chat(message: Message):
    user_id = message.from_user.id
    location = await redis.get(f"user:location:{user_id}")

    if not location:
        await message.answer("❗ Avval location aniqlanishi kerak.")
        return

    result = await start_search(user_id, location)

    if not result:
        await message.answer("⏳ Suhbatdosh kutilmoqda...")
        return

    user_a, user_b = result
    await message.bot.send_message(user_a, "✅ Suhbat boshlandi!", reply_markup=chat_kb)
    await message.bot.send_message(user_b, "✅ Suhbat boshlandi!", reply_markup=chat_kb)


# 2️⃣ ⏭ KEYINGI SUHBATDOSH
@router.message(F.text == "⏭ Keyingi")
async def next_chat(message: Message):
    user_id = message.from_user.id
    location = await redis.get(f"user:location:{user_id}")

    peer = await stop_chat(user_id)

    if peer:
        await message.bot.send_message(peer, "⏭ Suhbatdosh keyingi suhbatga o‘tdi.")

    await message.answer("🔄 Yangi suhbatdosh qidirilmoqda...")

    result = await start_search(user_id, location)
    if result:
        user_a, user_b = result
        await message.bot.send_message(user_a, "✅ Yangi suhbat boshlandi!", reply_markup=chat_kb)
        await message.bot.send_message(user_b, "✅ Yangi suhbat boshlandi!", reply_markup=chat_kb)


@router.message(F.text == "⛔ To‘xtatish")
async def stop(message: Message):
    user_id = message.from_user.id
    peer = await stop_chat(user_id)

    await message.answer("❌ Chat to‘xtatildi.")

    if peer:
        await message.bot.send_message(peer, "❌ Suhbatdosh chatni to‘xtatdi.")


@router.message()
async def forward_message(message: Message):
    user_id = message.from_user.id
    peer = await redis.get(f"chat:{user_id}")

    if not peer:
        return

    if message.from_user.is_bot:
        return

    if not message.text:
        return

    await message.bot.send_message(int(peer), message.text)
