from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.habits import HabitCreate, HabitRead, HabitUpdate
from app.crud import crud_habits
from app.db.database import get_db

from app.dependencies.user import get_user_id
from app.utils.habits import get_habit_or_err

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.get("/", response_model=List[HabitRead])
def read_habits(
  user_id: int = Depends(get_user_id),
  skip: int = 0, 
  limit: int = 100, 
  db: Session = Depends(get_db)):

  return crud_habits.get_habits(db, user_id=user_id, skip=skip, limit=limit)

@router.post("/", response_model=HabitRead, status_code=201)
def create_habit(
  habit: HabitCreate, 
  user_id: int = Depends(get_user_id), 
  db: Session = Depends(get_db)):

  try:
    return crud_habits.create_habit(db, habit, user_id=user_id)
  except SQLAlchemyError as err:
    db.rollback()
    print(f"[ERRO] Erro ao criar HABITO: {err}")
    raise
  
@router.get("/{habit_id}", response_model = HabitRead)
def read_habit(
  habit_id: int, 
  user_id: int = Depends(get_user_id), 
  db: Session = Depends(get_db)):

  get_habit_or_err(db, habit_id, user_id)
  habit = crud_habits.get_habit(db, habit_id)
  return habit

@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(
  habit_id: int, 
  habit_data: HabitUpdate, 
  user_id: int = Depends(get_user_id), 
  db: Session = Depends(get_db)):

  get_habit_or_err(db, habit_id, user_id)
  habit = crud_habits.update_habit(db, habit_id, habit_data)
  return habit
  

@router.delete("/{habit_id}",  status_code=204)
def delete_habit(
  habit_id: int, 
  user_id: int = Depends(get_user_id), 
  db:Session = Depends(get_db)):
  
  get_habit_or_err(db, habit_id, user_id)
  habit = crud_habits.delete_habit(db, habit_id)
