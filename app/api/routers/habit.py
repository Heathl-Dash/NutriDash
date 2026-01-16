from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud import crud_habits
from app.db.database import get_db
from app.dependencies.user import get_keycloak_id
from app.schemas.habits import HabitCreate, HabitRead, HabitUpdate
from app.utils.habits import get_habit_or_err

import uuid

habit_router = APIRouter()


@habit_router.get("/", response_model=List[HabitRead])
def read_habits(
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    skip: int = 0,
    limit: int = 100,
    positive: Optional[bool] = Query(None),
    negative: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):

    return crud_habits.get_habits(
        db,
        keycloak_id=keycloak_id,
        skip=skip,
        limit=limit,
        positive=positive,
        negative=negative,
    )


@habit_router.post("/", response_model=HabitRead, status_code=201)
def create_habit(
    habit: HabitCreate,
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    db: Session = Depends(get_db),
):

    try:
        return crud_habits.create_habit(db, habit, keycloak_id=keycloak_id)
    except SQLAlchemyError as err:
        db.rollback()
        print(f"[ERRO] Erro ao criar HABITO: {err}")
        raise


@habit_router.get("/{habit_id}", response_model=HabitRead)
def read_habit(
    habit_id: int, keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)
):

    get_habit_or_err(db, habit_id, keycloak_id)
    habit = crud_habits.get_habit(db, habit_id)
    return habit


@habit_router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    db: Session = Depends(get_db),
):

    get_habit_or_err(db, habit_id, keycloak_id)
    habit = crud_habits.update_habit(db, habit_id, habit_data)
    return habit


@habit_router.delete("/{habit_id}", status_code=204)
def delete_habit(
    habit_id: int, keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)
):

    get_habit_or_err(db, habit_id, keycloak_id)
    crud_habits.delete_habit(db, habit_id)
    return


@habit_router.patch("/{habit_id}/add-positive-counter", response_model=HabitRead)
def add_positive_count(
    habit_id: int, keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)
):

    habit = get_habit_or_err(db, habit_id, keycloak_id)

    if not habit.positive:
        raise HTTPException(
            status_code=400,
            detail=(
                "Este hábito não aceita contagem positiva. "
                "Apenas hábitos marcados como positivos"
                " ou mistos podem ter contagem positiva."
            ),
        )

    habit.positive_count += 1
    db.commit()
    db.refresh(habit)
    return habit


@habit_router.patch("/{habit_id}/add-negative-counter", response_model=HabitRead)
def add_negative_count(
    habit_id: int, keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)
):
    habit = get_habit_or_err(db, habit_id, keycloak_id)

    if not habit.negative:
        raise HTTPException(
            status_code=400,
            detail=(
                "Este hábito não aceita contagem negativa. "
                "Apenas hábitos marcados como negativos"
                " ou mistos podem ter contagem negativa."
            ),
        )

    habit.negative_count += 1
    db.commit()
    db.refresh(habit)
    return habit
