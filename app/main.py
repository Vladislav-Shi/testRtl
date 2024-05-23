from aiogram import Bot, Dispatcher

from app.config import settings
from app.handlers import register_routes

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

register_routes(dp)


async def main() -> None:
    await dp.start_polling(bot)
