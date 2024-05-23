from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings


def get_mongo_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.get_mongo_uri())
