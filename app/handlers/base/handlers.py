import json

from aiogram import Router, F
from aiogram.types import Message

from app.handlers.base.text import WRONG_TEXT
from utils.salary_aggregation.salary_aggregation import MongoAggregator
from utils.storage.mongo import get_mongo_client

router = Router()


@router.message(F.text)
async def hello_world(message: Message):
    try:
        data: dict = json.loads(message.text)  # type: ignore
        result = await MongoAggregator(client=get_mongo_client()).get_salary(
            dt_from=data['dt_from'],
            dt_upto=data['dt_upto'],
            group_type=data['group_type']
        )
        await message.answer(json.dumps(result))
    except Exception:
        await message.answer(WRONG_TEXT)
