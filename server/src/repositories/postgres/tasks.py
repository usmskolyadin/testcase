from dataclasses import dataclass
from typing import Iterable

from src.models.auth import User
from sqlalchemy import Executable, select, func, delete

from src.dtos.tasks import (
    CreateTaskRequestDTO,
    CreateTaskResponseDTO,
    TaskRequestDTO,
    TaskResponseDTO,
    TasksResponseDTO,
    UserTaskRequestDTO,
)
from src.models.tasks import Task
from src.repositories.postgres.base import SQLAlchemyRepository


@dataclass
class TasksRepository(SQLAlchemyRepository):
    async def get_all_tasks(self) -> TasksResponseDTO:
        query: Executable = select(Task)
        models: Iterable[Task] = await self.scalars(query)
        return TasksResponseDTO(items=[TaskResponseDTO.from_orm(model) for model in models])

    async def get_my_tasks(self, user_id) -> TasksResponseDTO:
        query: Executable = select(Task).where(Task.user.has(User.id == user_id))
        models: Iterable[Task] = await self.scalars(query)
        return TasksResponseDTO(items=[TaskResponseDTO.from_orm(model) for model in models])
    
    async def create_task(self, task: CreateTaskRequestDTO) -> CreateTaskResponseDTO:
        model = Task(
            message=task.message,
            user_id=task.user_id,
        )
        await self.add(model)
        return CreateTaskResponseDTO(id=model.id)


def init_tasks_repository() -> TasksRepository:
    return TasksRepository()
