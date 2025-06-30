from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.waterGoal import (
  WaterGoalRead, 
  WaterGoalCreate, 
  WaterGoalUpdate,
  WaterIntakeRead,
  WaterIntakeCreate
)
from app.crud import crud_water_goal
from app.db.database import get_db
from app.dependencies.user import get_user_id
from app.utils.water_goal import get_water_goal_or_err

router = APIRouter(prefix="/water_goal", tags=["WaterGoal"])

@router.get("/", response_model=WaterGoalRead, status_code=201)
def read_water_goal(
  user_id: int = Depends(get_user_id), 
  db: Session = Depends(get_db)):

    return get_water_goal_or_err(db, user_id)

@router.post("/", response_model=WaterGoalRead, status_code=201)
def create_water(
  water_goal:WaterGoalCreate, 
  user_id: int = Depends(get_user_id), 
  db: Session = Depends(get_db)):
    
    try:
      return crud_water_goal.create_water_goal(db, user_id, water_goal)
    except SQLAlchemyError as err:
      db.rollback()
      print(f"[ERRO] Erro ao criar WATER GOAL: {err}")
      raise

@router.patch("/", response_model=WaterGoalRead, status_code=201)
def update_water_goal(
  water_goal_data:WaterGoalUpdate, 
  user_id: int = Depends(get_user_id), 
  db:Session = Depends(get_db)):
    
    get_water_goal_or_err(db, user_id)
    water_goal = crud_water_goal.update_water_goal(db, user_id, water_goal_data)
    return water_goal
  

@router.delete("/", status_code=204)
def delete_water_goal(
   user_id: int = Depends(get_user_id), 
   db: Session = Depends(get_db)):
    
    get_water_goal_or_err(db, user_id)
    water_goal = crud_water_goal.delete_water_goal(db, user_id)
    return water_goal


@router.post("/intakes/", response_model=WaterIntakeRead)
def register_intake(
    intake_data: WaterIntakeCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id),
):
    return crud_water_goal.create_intake(db, intake_data, user_id)


@router.get("/intakes/", response_model=list[WaterIntakeRead])
def list_user_intakes(
    user_id: int = Depends(get_user_id), 
    db: Session = Depends(get_db)
):
    return crud_water_goal.get_intakes_by_user(db, user_id)