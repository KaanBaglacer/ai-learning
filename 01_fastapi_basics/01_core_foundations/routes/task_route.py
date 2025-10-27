from fastapi import APIRouter, Depends, HTTPException
from typing import Sequence
from sqlmodel import Session

from config.config import get_session
from entity.task import Task
from service.task_service import get_task as crud_get_task
from service.task_service import get_tasks as crud_get_tasks
from service.task_service import create_task as crud_create_task
from service.task_service import update_task as crud_update_task
from service.task_service import delete_task as crud_delete_task

router = APIRouter()

@router.get("/tasks", response_model=Sequence[Task])
async def list_tasks(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    return crud_get_tasks(session, offset=offset, limit=limit)


@router.get("/tasks/{task_id}", response_model=Task)
async def read_task(task_id: int, session: Session = Depends(get_session)):
    return crud_get_task(session, task_id)


@router.post("/add-task", response_model=Task)
async def add_task(item: Task, session: Session = Depends(get_session)):
    return crud_create_task(session, item)

@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, item: Task, session: Session = Depends(get_session)):
    updated_task = crud_update_task(session, task_id, item)
    if updated_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    success = crud_delete_task(session, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": True}
