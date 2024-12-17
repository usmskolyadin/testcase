from dataclasses import dataclass
from src.repositories.mongo.base import get_collection
from src.dtos.auth import UserRequestDTO
from src.dtos.tasks import (
    CreateTaskRequestDTO, CreateTaskResponseDTO, MongoDBCreateTaskRequestDTO,
    TaskResponseDTO, TaskRequestDTO, TasksResponseDTO
)
from src.repositories.mongo.tasks import MongoDBTasksRepository, init_mongodb_tasks_repository


@dataclass
class MongoDBTaskService:
    mongodb_task_repository: MongoDBTasksRepository

    async def get_my_tasks(self, user_id: UserRequestDTO) -> TasksResponseDTO:
        return await self.mongodb_task_repository.get_my_tasks(user_id=user_id)

    async def get_all_tasks(self) -> TasksResponseDTO:
        return await self.mongodb_task_repository.get_all_tasks()
    
    async def add_task(
        self,
        id: int,
        message: str,
        user_id: UserRequestDTO
    ) -> int:
        task_dto = MongoDBCreateTaskRequestDTO(
            id=id,
            message=message,
            user_id=user_id
        )   

        task = await self.mongodb_task_repository.create_task(task=task_dto)
        return TaskResponseDTO(
            id=id,
            message=message,
            user_id=user_id,
        )

async def get_mongodb_task_service() -> MongoDBTaskService:
    mongodb_task_repository = await init_mongodb_tasks_repository() 
    return MongoDBTaskService(mongodb_task_repository=mongodb_task_repository)
