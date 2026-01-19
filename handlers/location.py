from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from storage.redis import redis

router = Router()

chat_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="💬 Chatni boshlash")]],
    resize_keyboard=True
)

@router.message(F.contact)
async def handle_contact(message: Message):
    phone = message.contact.phone_number.replace(" ", "")

    if phone.startswith("+998"):
        location = "uz"
    elif phone.startswith("+82"):
        location = "kr"
    elif phone.startswith("+7"):
        location = "ru"
    else:
        location = None

    if not location:
        await message.answer("❌ Sizning davlatingiz qo‘llab-quvvatlanmaydi.")
        return

    # 🔑 ENG MUHIM QATOR
    await redis.set(f"user:location:{message.from_user.id}", location)

    await message.answer(
        f"📍 Location aniqlandi: {location.upper()}\n"
        "Endi anonim chatni boshlashingiz mumkin.",
        reply_markup=chat_kb
    )
