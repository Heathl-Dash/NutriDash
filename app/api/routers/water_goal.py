from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.waterGoal import WaterGoalRead, WaterGoalCreate, WaterGoalUpdate
from app.crud import crud_water_goal
from app.db.database import get_db

router = APIRouter(prefix="/water_goal", tags=["WaterGoal"])

@router.get("/{user_id}", response_model=WaterGoalRead, status_code=201)
def read_water_goal(user_id: int, db: Session = Depends(get_db)):
  water_goal = crud_water_goal.get_water_goal(db, user_id)
  if not water_goal:
    raise HTTPException(status_code=404, detail="Water GOAl not found")
  return water_goal
