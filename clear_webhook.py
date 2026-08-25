import sys
import asyncio

# Ensure package path so config can be imported
sys.path.insert(0, "ethio-car-equb/ethio-car-equb")

from config import BOT_TOKEN
from aiogram import Bot


async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        print("Webhook cleared successfully.")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
