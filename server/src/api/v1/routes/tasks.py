from fastapi import UploadFile, File, APIRouter, Depends, status, HTTPException

from src.utils.auth import get_current_user
from src.api.v1.schemas.tasks import (
    SCreateTaskResponse, STaskRequest, STaskResponse, STasksResponse, User,
)
from src.services.postgres.tasks import get_task_service
from src.services.mongo.tasks import get_mongodb_task_service


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    path="/submit",
    summary="Submit data to the server",
    response_model=SCreateTaskResponse,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": SCreateTaskResponse}},
)
async def create_task(
    data: STaskRequest,
    user: User = Depends(get_current_user),
) -> SCreateTaskResponse:

    service = get_task_service()
    task = await service.add_task(
        user_id=user.id,
        message=data.message
    )

    # service_log = await get_mongodb_task_service()
    # try:
    #     task_log = await service_log.add_task(
    #         id=task.id,
    #         message=data.message,
    #         user_id=user.id
    #     )
    # except Exception as e:
    #     print(f"Error during task insertion: {e}")
    #     raise HTTPException(status_code=500, detail="Internal Server Error")
    
    # print(task_log)
    
    return SCreateTaskResponse(id=task.id)

@router.get(
    path="/tasks",
    summary="Submit data to the server",
    response_model=STasksResponse,
    status_code=status.HTTP_200_OK,
    # responses={status.HTTP_200_OK: {"models": STasksResponse}},
)
async def get_all_tasks(
) -> STasksResponse:
    service = get_task_service()
    tasks = await service.get_all_tasks()

    items = list(map(
        lambda task: STaskResponse(
            id=task.id,
            message=task.message,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        ),
        tasks.items
    ))

    return STasksResponse(items=items)


@router.get(
    path="/tasks/my",
    summary="Submit data to the server",
    response_model=STasksResponse,
    status_code=status.HTTP_200_OK,
    # responses={status.HTTP_200_OK: {"model": STaskResponse}},
)
async def get_my_tasks(
    user: User = Depends(get_current_user), 
) -> STasksResponse:
    service = get_task_service()
    tasks = await service.get_my_tasks(user_id=user.id)
    print(f" FSDDSFJKSDFLDSFJSLDFJLKSD {user.id}")
    items = list(map(
        lambda task: STaskResponse(
            id=task.id,
            message=task.message,
            user_id=task.user_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
        ),
        tasks.items
    ))
    print(items)
    return STasksResponse(items=items)