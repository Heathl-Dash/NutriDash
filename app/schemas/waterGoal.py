from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class WaterGoalBase(BaseModel):
    pass


class WaterGoalCreate(WaterGoalBase):
    ml_drinked: Optional[int] = None
    weight: Optional[float] = None


class WaterGoalUpdate(BaseModel):
    ml_goal: Optional[int] = None
    ml_drinked: Optional[int] = None
    weight: Optional[float] = None


class WaterBottleBase(BaseModel):
    bottle_name: str
    ml_bottle: int


class WaterBottleCreate(WaterBottleBase):
    pass

class WaterBottleRead(WaterBottleBase):
    id_bottle_style: int
    user_id:int
    water_bottle_id: int

    class Config:
        orm_mode = True

class WaterBottleUpdate(BaseModel):
    bottle_name: Optional[str] = None
    ml_bottle: Optional[int] = None


class WaterGoalRead(WaterGoalBase):
    ml_goal: int
    water_goal_id: int
    ml_drinked: Optional[int] = None
    bottles: List[WaterBottleRead] = []
    last_updated: datetime

    class Config:
        orm_mode = True