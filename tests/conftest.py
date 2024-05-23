import json
from pathlib import Path

import pytest
from bson import json_util
from mongomock_motor import AsyncMongoMockClient  # type: ignore

TEST_DIR = BASE_DIR = Path(__file__).resolve().parent


@pytest.fixture
async def client():
    client = AsyncMongoMockClient()
    collection = client["sampleDB"]["sample_collection"]
    with open(TEST_DIR / 'data' / 'sample_collection.json', 'r') as file:
        data = json.load(file, object_hook=json_util.object_hook)
    await collection.insert_many(data)
    return client
