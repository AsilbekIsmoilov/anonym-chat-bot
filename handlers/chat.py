from aiogram import Router, F
from aiogram.types import Message
from storage.redis import redis
from services.matcher import start_search

router = Router()

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

    await message.bot.send_message(user_a, "✅ Suhbat boshlandi!")
    await message.bot.send_message(user_b, "✅ Suhbat boshlandi!")


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

    await message.bot.send_message(
        chat_id=int(peer),
        text=message.text
    )
