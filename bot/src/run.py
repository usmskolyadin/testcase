import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.core.config import settings

global_state = {}


bot = Bot(settings.telegram_api_key, timeout=120)
dp = Dispatcher()
logging.basicConfig(level=logging.DEBUG)

async def main():
    from src.handlers.start import start_router
    from src.handlers.dashboard import dashboard_router
    from src.handlers.stats import stats_router


    dp.include_router(start_router)
    dp.include_router(dashboard_router)
    dp.include_router(stats_router)
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())