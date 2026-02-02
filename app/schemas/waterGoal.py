from datetime import datetime
from typing import List, Optional
from uuid import UUID

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
    id_bottle_style: Optional[int] = None


class WaterBottleCreate(WaterBottleBase):
    pass


class WaterBottleRead(WaterBottleBase):
    water_bottle_id: int
    keycloak_id: UUID

    class Config:
        orm_mode = True


class WaterBottleUpdate(BaseModel):
    bottle_name: Optional[str] = None
    ml_bottle: Optional[int] = None
    id_bottle_style: int


class WaterGoalRead(WaterGoalBase):
    ml_goal: int
    water_goal_id: int
    ml_drinked: Optional[int] = None
    bottles: List[WaterBottleRead] = []
    last_updated: datetime

    class Config:
        orm_mode = True


class WaterIntakeBase(BaseModel):
    water_goal_id: int
    ml: int


class WaterIntakeCreate(WaterIntakeBase):
    pass


class WaterIntakeRead(BaseModel):
    id: int
    keycloak_id: UUID
    water_goal_id: int
    ml: int
    timestamp: datetime

    class Config:
        orm_mode = True


class WaterIntakeSummary(BaseModel):
    date: str
    total_ml: int
