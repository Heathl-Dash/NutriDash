from typing import Optional
from pydantic import BaseModel

class ToDoBase(BaseModel):
    title: str
    description: str

class ToDoCreate(ToDoBase):
    pass

class ToDoRead(ToDoBase):
    todo_id: int
    done: bool

    class Config:
        orm_mode = True

class ToDoUpdate(ToDoBase):
    title: Optional[str]
    description: Optional[str]
    done: Optional[bool]