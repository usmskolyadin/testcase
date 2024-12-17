from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Any, List

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql import Executable

from src.core.config import settings
from src.models.base import Base
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from motor.motor_asyncio import AsyncIOMotorClient


async def get_collection() -> AsyncIOMotorCollection:
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client['mydatabase']
    return db['mytasks'] 

@dataclass
class MongoDBRepository:
    collection: AsyncIOMotorCollection
    
    async def add(self, obj: dict) -> str:
        result = await self.collection.insert_one(obj)
        return str(result.inserted_id)

    async def find(self, filter: dict) -> List[dict]:
        return [task async for task in self.collection.find(filter)]

    async def get(self, filter: dict) -> dict:
        return await self.collection.find_one(filter)