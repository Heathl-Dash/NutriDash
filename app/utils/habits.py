import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_habits


def get_habit_or_err(db: Session, habit_id: int, keycloak_id: uuid.UUID):
    habit = crud_habits.get_habit(db, habit_id)

    if not habit:
        raise HTTPException(status_code=404, detail="HABIT not found")

    if habit.keycloak_id != keycloak_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this HABIT"
        )

    return habit
