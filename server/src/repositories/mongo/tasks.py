from dataclasses import dataclass
from src.dtos.tasks import (
    CreateTaskRequestDTO,
    CreateTaskResponseDTO,
    MongoDBCreateTaskRequestDTO,
    TaskResponseDTO,
    TasksResponseDTO,
)
from src.repositories.mongo.base import MongoDBRepository, get_collection
from motor.motor_asyncio import AsyncIOMotorCollection


@dataclass
class MongoDBTasksRepository(MongoDBRepository):
    async def get_all_tasks(self) -> TasksResponseDTO:
        models = await self.find({})
        return TasksResponseDTO(items=[TaskResponseDTO(**model) for model in models])

    async def get_my_tasks(self, user_id: str) -> TasksResponseDTO:
        models = await self.find({'user_id': user_id})
        return TasksResponseDTO(items=[TaskResponseDTO(**model) for model in models])

    async def create_task(self, task: MongoDBCreateTaskRequestDTO) -> CreateTaskResponseDTO:
        model = {
            'id': str(task.id),
            'message': task.message,
            'user_id': task.user_id,
        }
        task_id = await self.add(model)
        return CreateTaskResponseDTO(id=task_id)

async def init_mongodb_tasks_repository() -> MongoDBTasksRepository:
    collection = await get_collection()
    return MongoDBTasksRepository(collection=collection)
