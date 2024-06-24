# import libraries
from aiogram import Bot, Dispatcher
import asyncio
# import bot configuration
from config import TOKEN
# import function that creates all tables in database
from app.database.models import async_main
from app.hanlders import router
import logging


# main function that sets bot
async def main():
    # creates tables in database
    await async_main()
    # connects to bot
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    # setting messages router filter
    dp.include_router(router)
    # starts bot
    await dp.start_polling(bot)


# checking if file runs from main moduile
if __name__ == '__main__':
    # connecting logging
    logging.basicConfig(level=logging.INFO)
    try:
        # asyncio - runs bot in asynchronous mode
        asyncio.run(main())
    # checks KeyboardInterrupt error
    except KeyboardInterrupt:
        print('Exit')
