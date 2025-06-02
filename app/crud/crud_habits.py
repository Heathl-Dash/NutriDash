from sqlalchemy.orm import Session
from app.models.habits import Habit
from app.schemas.habits import HabitCreate, HabitUpdate

def get_habit(db: Session, habit_id: int):
  return db.query(Habit).filter(Habit.habit_id == habit_id).first()

def get_habits(db:Session, user_id: int, skip: int = 0, limit: int = 100):
  return db.query(Habit).filter(Habit.user_id == user_id).offset(skip).limit(limit).all()


def create_habit(db:Session, habit:HabitCreate, user_id: int):
  db_habit = Habit(**habit.model_dump(), user_id = user_id)
  db.add(db_habit)
  db.commit()
  db.refresh(db_habit)
  return db_habit


def update_habit(db: Session, habit_id: int, habit_data: HabitUpdate):
  db_habit = get_habit(db, habit_id)
  if not db_habit:
    return None
  for key, value in habit_data.dict(exclude_unset=True).items():
    setattr(db_habit, key, value)
  db.commit()
  db.refresh(db_habit)
  return db_habit


def delete_habit(db: Session, habit_id):
  db_habit = get_habit(db, habit_id)
  if not db_habit:
    return None
  db.delete(db_habit)
  db.commit()
  return db_habit