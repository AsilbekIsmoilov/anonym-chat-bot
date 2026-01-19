from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

@router.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer(
        "Salom! Anonim chat.py botga xush kelibsiz.\n"
        "Davlatingizni aniqlash uchun telefon raqamingizni yuboring.",
        reply_markup=contact_kb
    )
