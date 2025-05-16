from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_db
from models import Task
from request import TaskCreateRequest, TaskUpdateRequest
from response import TaskResponse


task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("/{id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_by_id(id: int, session: AsyncSession = Depends(get_db)):
    task = await session.get(Task, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id = {id} not found",
        )

    return task


@task_router.post(
    "/create", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def create(
    task_create: TaskCreateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        task = Task(**task_create.model_dump())
        session.add(task)
        await session.commit()
        await session.refresh(task)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))

    return task


@task_router.patch(
    "/update", response_model=TaskResponse, status_code=status.HTTP_200_OK
)
async def update(
    id: int, task_update: TaskUpdateRequest, session: AsyncSession = Depends(get_db)
):
    try:
        task = await session.get(Task, id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id = {id} not found",
            )

        if task_update.title:
            task.title = task_update.title
        if task_update.content:
            task.content = task_update.content
        if task_update.status:
            task.status = task_update.status

        await session.commit()
        await session.refresh(task)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
    return task


@task_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete(id: int, session: AsyncSession = Depends(get_db)):
    try:
        task = await session.get(Task, id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id = {id} not found",
            )
        await session.delete(task)
        await session.commit()
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))
