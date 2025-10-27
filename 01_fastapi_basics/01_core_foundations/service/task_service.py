
from datetime import datetime, timezone
from typing import Sequence, cast
from sqlmodel import select
from sqlmodel import Session
from entity.task import Task


def get_tasks(session: Session, offset: int = 0, limit: int = 100) -> Sequence[Task]:
    return session.exec(select(Task).offset(offset).limit(limit)).all()

def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)

def create_task(session: Session, item: Task) -> Task:
    now = datetime.now(timezone.utc)
    if item.createdAt is None:
        item.createdAt = now
    item.updatedAt = now
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


def update_task(session: Session, task_id: int, item: Task) -> Task | None:
    existing_task = cast(Task | None, session.get(Task, task_id))
    if not existing_task:
        return None

    protected = {"id", "createdAt", "updatedAt"}
    updates = item.model_dump(exclude_unset=True)
    for key, value in updates.items():
        if key in protected:
            continue
        setattr(existing_task, key, value)
    existing_task.updatedAt = datetime.now(timezone.utc)
    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task

def delete_task(session: Session, task_id: int) -> bool:
    existing_task = cast(Task | None, session.get(Task, task_id))
    if not existing_task:
        return False

    session.delete(existing_task)
    session.commit()
    return True
