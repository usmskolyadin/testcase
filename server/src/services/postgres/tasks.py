from dataclasses import dataclass
from src.dtos.auth import UserRequestDTO
from src.dtos.tasks import (
    CreateTaskRequestDTO, CreateTaskResponseDTO,
    TaskResponseDTO, TaskRequestDTO, TasksResponseDTO
)
from src.repositories.postgres.tasks import TasksRepository, init_tasks_repository


@dataclass
class TaskService:
    task_repository: TasksRepository

    async def get_my_tasks(self, user_id: UserRequestDTO) -> TasksResponseDTO:
        return await self.task_repository.get_my_tasks(user_id=user_id)

    async def get_all_tasks(self) -> TasksResponseDTO:
        return await self.task_repository.get_all_tasks()
    
    async def add_task(
        self,
        message: str,
        user_id: UserRequestDTO
    ) -> int:
        task_dto = CreateTaskRequestDTO(
            message=message,
            user_id=user_id
        )   

        task = await self.task_repository.create_task(task=task_dto)
        return CreateTaskResponseDTO(
            id=task.id,
        )

def get_task_service(task_repository: TasksRepository = init_tasks_repository()) -> TaskService:
    task_service = TaskService(task_repository=task_repository)
    return task_service
