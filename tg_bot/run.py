import asyncio
import logging

from config import bot, dp

logging.basicConfig(level=logging.DEBUG)


async def on_startup():
    pass


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
