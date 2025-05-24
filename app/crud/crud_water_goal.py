from sqlalchemy.orm import Session
from app.models.waterGoal import WaterGoal
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate


def get_water_goal(db: Session, user_id:int):
  return db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()

def get_water_goal_by_user(db: Session, user_id: int):
  return db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()


def create_water_goal(db: Session, water_goal:WaterGoalCreate):
  db_water_goal = WaterGoal(**water_goal.model_dump())
  db.add(db_water_goal)
  db.commit()
  db.refresh(db_water_goal)
  return db_water_goal

def update_water_goal(db: Session, user_id: int, water_goal_data:WaterGoalUpdate):
  db_water_goal = get_water_goal(db, user_id)
  if not db_water_goal:
    return None
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