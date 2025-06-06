from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class ToDoBase(BaseModel):
    title: str
    description: str

class ToDoCreate(ToDoBase):
    pass

class ToDoRead(ToDoBase):
    user_id: int
    todo_id: int
    done: bool
    created: datetime

    class Config:
        orm_mode = True

class ToDoUpdate(ToDoBase):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None