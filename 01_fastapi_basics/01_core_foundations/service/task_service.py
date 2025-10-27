
from datetime import datetime, timezone
from typing import Sequence
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