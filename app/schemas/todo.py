from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ToDoBase(BaseModel):
    title: str
    description: str


class ToDoCreate(ToDoBase):
    pass


class ToDoRead(ToDoBase):
    keycloak_id: UUID
    id: int
    done: bool
    created: datetime

    class Config:
        orm_mode = True


class ToDoUpdate(ToDoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


class ToDoHistoryBase(BaseModel):
    todo_id: int
    keycloak_id: UUID


class ToDoHistoryCreate(ToDoHistoryBase):
    date_done: datetime | None = None


class TodoHistoryRead(ToDoHistoryBase):
    to_do_history_id: int
    date_done: datetime

    class Config:
        orm_mode = True
