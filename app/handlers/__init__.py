from aiogram import Dispatcher

from .base.handlers import router as base_router


def register_routes(dp: Dispatcher):
    dp.include_router(base_router)
