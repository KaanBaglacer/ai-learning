from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Boolean, TIMESTAMP, func

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, title="Task ID")
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=500)
    isCompleted: bool = Field(default=False, sa_column=Column("is_completed", Boolean, nullable=False))
    createdAt: datetime | None = Field(
        default=None,
        sa_column=Column("created_at", TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
    )
    updatedAt: datetime | None = Field(
        default=None,
        sa_column=Column(
            "updated_at",
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
            onupdate=func.now(),
        ),
    )