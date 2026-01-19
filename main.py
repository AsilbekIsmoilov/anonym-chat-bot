import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from loguru import logger

from handlers import start,location,chat

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN not found")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_router(start.router)
dp.include_router(location.router)
dp.include_router(chat.router)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Bot starting...")
    task = asyncio.create_task(dp.start_polling(bot))
    yield
    logger.info("Bot stopping...")
    task.cancel()


app = FastAPI(
    title="Anonim Chat Bot",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok"}
