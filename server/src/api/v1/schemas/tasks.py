from datetime import date, datetime
from typing import List
from pydantic import BaseModel, EmailStr


class STaskRequest(BaseModel):
    message: str

class STaskResponse(BaseModel):
    id: int
    message: str
    user_id: int
    created_at: datetime
    updated_at: datetime


class SCreateTaskResponse(BaseModel):
    id: int

class STasksResponse(BaseModel):
    items: List[STaskResponse]


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    message: str
    tasks: "User"