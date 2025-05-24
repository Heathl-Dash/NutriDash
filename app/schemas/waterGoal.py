from typing import Optional, List
from pydantic import BaseModel


class WaterGoalBase(BaseModel):
    ml_goal: int


class WaterGoalCreate(WaterGoalBase):
    user_id: Optional[int] = None


class WaterGoalUpdate(BaseModel):
    ml_goal: Optional[int] = None
    ml_drinked: Optional[int] = None


class WaterBottleBase(BaseModel):
    bottle_name: str
    ml_bottle: int


class WaterBottleCreate(WaterBottleBase):
    pass

class WaterBottleRead(WaterBottleBase):
    water_bottle_id: int
    water_goal_id: int

    class Config:
        orm_mode = True

class WaterBottleUpdate(BaseModel):
    bottle_name: Optional[str] = None
    ml_bottle: Optional[int] = None


class WaterGoalRead(WaterGoalBase):
    water_goal_id: int
    ml_drinked: Optional[int] = None
    bottles: List[WaterBottleRead] = []

    class Config:
        orm_mode = True