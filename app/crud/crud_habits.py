from sqlalchemy.orm import Session
from app.models.habits import Habit
from app.schemas.habits import HabitCreate, HabitUpdate

def get_habit(db: Session, habit_id: int):
  return db.query(Habit).filter(Habit.habit_id == habit_id).first()

def get_habits(db:Session, skip: int = 0, limit: int = 100):
  return db.query(Habit).offset(skip).limit(limit).all()


def create_habit(db:Session, habit:HabitCreate):
  db_habit = Habit(**habit.model_dump())
  db.add(db_habit)
  db.commit()
  db.refresh(db_habit)
  return db_habit


