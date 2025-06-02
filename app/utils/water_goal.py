from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import crud_water_goal


def get_water_goal_or_err(db: Session, user_id: int):
  water_goal = crud_water_goal.get_water_goal(db, user_id)

  if not water_goal:
    raise HTTPException(status_code=404, detail="water_goal not found")
  
  if water_goal.user_id != user_id:
    raise HTTPException(status_code=403, detail="Not authorized to access this water_goal")


  return water_goal