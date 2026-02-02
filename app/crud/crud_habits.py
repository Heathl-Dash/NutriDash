from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.habits import Habit
from app.schemas.habits import HabitCreate, HabitUpdate

import uuid


def get_habit(db: Session, habit_id: int):
    return db.query(Habit).filter(Habit.id == habit_id).first()


def get_habits(
    db: Session,
    keycloak_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    positive: Optional[bool] = None,
    negative: Optional[bool] = None,
):

    query = db.query(Habit).filter(Habit.keycloak_id == keycloak_id)

    if positive is True:
        query = query.filter(Habit.positive.is_(True))

    if negative is True:
        query = query.filter(Habit.negative.is_(True))

    return query.order_by(Habit.created.desc()).offset(skip).limit(limit).all()


def create_habit(db: Session, habit: HabitCreate, keycloak_id: uuid.UUID):
    if habit.negative is False and habit.positive is False:
        raise HTTPException(
            status_code=400,
            detail="O hábito tem que ser marcado como positivo e/ou negativo.",
        )

    db_habit = Habit(**habit.model_dump(), keycloak_id=keycloak_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit


def update_habit(db: Session, habit_id: int, habit_data: HabitUpdate):
    db_habit = get_habit(db, habit_id)
    if not db_habit:
        return None
        
    new_positive = habit_data.positive if habit_data.positive is not None else db_habit.positive
    new_negative = habit_data.negative if habit_data.negative is not None else db_habit.negative
    
    if not new_positive and not new_negative:
        raise HTTPException(
            status_code=400, 
            detail="Habit must be either positive, negative, or both"
        )            
        
    for key, value in habit_data.model_dump(exclude_unset=True).items():
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


def filter_positive_habits(db: Session, keycloak_id: uuid.UUID):
    positive_habits = (
        db.query(Habit).filter(Habit.positive.is_(True), Habit.keycloak_id == keycloak_id).all()
    )

    return positive_habits


def filter_negative_habits(db: Session, keycloak_id: uuid.UUID):
    positive_habits = (
        db.query(Habit).filter(Habit.negative.is_(True), Habit.keycloak_id == keycloak_id).all()
    )

    return positive_habits
