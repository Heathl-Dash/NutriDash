from sqlalchemy.orm import Session
from app.models.waterGoal import WaterGoal
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate

from fastapi import HTTPException
from datetime import datetime, date
from zoneinfo import ZoneInfo


def get_water_goal(db: Session, user_id:int):
  water_goal = db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()
  if not water_goal:
    return None

  now_local = datetime.now(ZoneInfo("America/Sao_Paulo"))
  today_local = now_local.date()

  if water_goal.last_updated.date() < today_local:
      water_goal.ml_drinked = 0
      water_goal.last_updated = now_local
      db.commit()
      db.refresh(water_goal)

  return water_goal


def get_water_goal_by_user(db: Session, user_id: int):
  return db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()

def create_water_goal(db: Session, user_id: int, water_goal:WaterGoalCreate):
  has_water_goal = get_water_goal_by_user(db, user_id)
  if(has_water_goal):
    raise HTTPException(status_code=400, detail="Water goal already exists for this user")

  if(water_goal.weight is not None and water_goal.weight > 0):
    daily_goal = round(water_goal.weight * 35)
  else:
    daily_goal = 2000

  data = water_goal.model_dump(exclude={"ml_goal", "weight"})

  db_water_goal = WaterGoal(**data, user_id = user_id, ml_goal=daily_goal)
  db.add(db_water_goal)
  db.commit()
  db.refresh(db_water_goal)
  return db_water_goal

def update_water_goal(db: Session, user_id: int, water_goal_data:WaterGoalUpdate):
  db_water_goal = get_water_goal(db, user_id)
  if not db_water_goal:
    return None

  if(water_goal_data.weight is not None and water_goal_data.weight > 0):
    db_water_goal.ml_goal = round(water_goal_data.weight * 35)
  else:
    db_water_goal.ml_goal = db_water_goal.ml_goal

  for key, value in water_goal_data.dict(exclude_unset=True).items():
    setattr(db_water_goal, key, value)
  db.commit()
  db.refresh(db_water_goal)
  return db_water_goal
    

def delete_water_goal(db: Session, user_id):
  db_water_goal = get_water_goal(db, user_id)
  if not db_water_goal:
    return None
  db.delete(db_water_goal)
  db.commit()
  return db_water_goal