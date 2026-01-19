from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

async def is_member(bot: Bot, user_id: int, group_id: int) -> bool:
    try:
        member = await bot.get_chat_member(group_id, user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramBadRequest:
        return False
