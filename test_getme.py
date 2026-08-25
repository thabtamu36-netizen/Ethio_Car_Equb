import sys
import asyncio
from aiogram import Bot

# ensure package path to import config
sys.path.insert(0, "ethio-car-equb/ethio-car-equb")
from config import BOT_TOKEN


async def main():
    bot = Bot(token=BOT_TOKEN)
    try:
        me = await bot.get_me()
        print("getMe OK:", me)
    except Exception as e:
        print("getMe ERROR:", type(e).__name__, e)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
