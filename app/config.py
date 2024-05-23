import logging
from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_LEVEL = [
    logging.WARNING,
    logging.DEBUG
]


class Settings(BaseSettings):

    BOT_TOKEN: str

    MONGO_HOST: str
    MONGO_PORT: str
    MONGO_USER: str
    MONGO_PASS: str

    def get_mongo_uri(self) -> str:
        return f'mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}/'

    class Config:
        env_file = Path(BASE_DIR, '.env')
        dotenv.load_dotenv(env_file)


settings = Settings()  # type: ignore
