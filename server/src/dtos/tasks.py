from datetime import datetime, date
from src.dtos.base import BaseRequestDTO, BaseResponseDTO


class TaskRequestDTO(BaseRequestDTO):
    id: str


class CreateTaskRequestDTO(BaseRequestDTO):
    message: str
    user_id: int

class MongoDBCreateTaskRequestDTO(BaseRequestDTO):
    id: int
    message: str
    user_id: int

class UserTaskRequestDTO(BaseRequestDTO):
    message: str
    user_id: int

class TaskResponseDTO(BaseResponseDTO):
    id: int
    message: str
    user_id: int
    created_at: datetime
    updated_at: datetime

class MongoTaskResponseDTO(BaseResponseDTO):
    id: int
    message: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class CreateTaskResponseDTO(BaseResponseDTO):
    id: int


class TaskDTO(BaseResponseDTO):
    id: int
    message: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class TasksResponseDTO(BaseResponseDTO):
    items: list[TaskDTO]