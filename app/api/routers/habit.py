from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.habits import HabitCreate, HabitRead, HabitUpdate
from app.crud import crud_habits
from app.db.database import get_db

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.get("/", response_model=List[HabitRead])
def read_habits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud_habits.get_habits(db, skip=skip, limit=limit)

@router.post("/", response_model=HabitRead, status_code=201)
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
  try:
    return crud_habits.create_habit(db, habit)
  except SQLAlchemyError as err:
    db.rollback()
    print(f"[ERRO] Erro ao criar HABITO: {err}")
    raise
  
@router.get("/{habit_id}", response_model = HabitRead)
def read_habit(habit_id: int, db: Session = Depends(get_db)):
  habit = crud_habits.get_habit(db, habit_id)
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  return habit

@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: int, habit_data: HabitUpdate, db: Session = Depends(get_db)):
  habit = crud_habits.update_habit(db, habit_id, habit_data)
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  return habit

@router.delete("/{habit_id}", response_model=HabitRead)
def delete_habit(habit_id: int, db:Session = Depends(get_db)):
  habit = crud_habits.delete_habit(db, habit_id)
  if not habit:
    raise HTTPException(status_code=404, detail="Habit not found")
  return habit