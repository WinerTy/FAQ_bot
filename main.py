from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import conf

from handlers.common_handlers import router
from handlers.menu_handlers import router as menu_router
from data import FAQ_DATA


async def main() -> Bot:
    bot = Bot(token=conf.bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    print(FAQ_DATA)
    dp.include_routers(router)
    dp.include_routers(menu_router)
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        import asyncio

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
