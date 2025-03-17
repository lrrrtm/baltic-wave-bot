import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv
from handlers import (start, my_cards, info, pay)

load_dotenv()

bot = Bot(token=os.getenv("BOT_API_TOKEN"), default=DefaultBotProperties(parse_mode='html'))
dp = Dispatcher()

dp.include_routers(
    start.router,
    my_cards.router,
    info.router,
    pay.router,
)
