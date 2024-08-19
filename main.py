import asyncio
from aiogram import Bot, Dispatcher
import logging
from config_reader import config
from handlers import bot_messages, user_comands, questionaire, callback_handlers
from middlewares.antiflood import AntiFloodMiddleware

async def main() -> None:
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware(0.1))

    dp.include_routers(
        user_comands.router,
        bot_messages.router,
        questionaire.router,
        callback_handlers.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exiting')
