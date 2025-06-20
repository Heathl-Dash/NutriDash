from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from datetime import datetime


class HabitBase(BaseModel):
    title: str
    description: str
    positive: bool  
    negative: bool

class HabitCreate(HabitBase):
    pass

class HabitRead(HabitBase):
    positive_count:int
    negative_count:int
    user_id: int
    habit_id: int
    created: datetime

    class Config:
        orm_mode = True

class HabitUpdate(HabitBase):
    title: Optional[str] = None
    description: Optional[str] = None
    positive: Optional[bool] = None
    negative: Optional[bool] = None
    positive_count: Optional[int] = None
    negative_count: Optional[int] = None