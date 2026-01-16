from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.crud import crud_water_goal
from app.db.database import get_db
from app.dependencies.user import get_keycloak_id
from app.schemas.waterGoal import (
    WaterGoalCreate,
    WaterGoalRead,
    WaterGoalUpdate,
    WaterIntakeCreate,
    WaterIntakeRead,
    WaterIntakeSummary,
)
from app.utils.water_goal import get_water_goal_or_err

import uuid

router = APIRouter()


@router.get("/", response_model=WaterGoalRead, status_code=201)
def read_water_goal(keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)):

    return get_water_goal_or_err(db, keycloak_id)


@router.post("/", response_model=WaterGoalRead, status_code=201)
def create_water(
    water_goal: WaterGoalCreate,
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    db: Session = Depends(get_db),
):

    try:
        return crud_water_goal.create_water_goal(db, keycloak_id, water_goal)
    except SQLAlchemyError as err:
        db.rollback()
        print(f"[ERRO] Erro ao criar WATER GOAL: {err}")
        raise


@router.patch("/", response_model=WaterGoalRead, status_code=201)
def update_water_goal(
    water_goal_data: WaterGoalUpdate,
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    db: Session = Depends(get_db),
):

    get_water_goal_or_err(db, keycloak_id)
    water_goal = crud_water_goal.update_water_goal(db, keycloak_id, water_goal_data)
    return water_goal


@router.delete("/", status_code=204)
def delete_water_goal(
    keycloak_id: uuid.UUID = Depends(get_keycloak_id), db: Session = Depends(get_db)
):

    get_water_goal_or_err(db, keycloak_id)
    water_goal = crud_water_goal.delete_water_goal(db, keycloak_id)
    return water_goal


@router.post("/intakes/", response_model=WaterIntakeRead)
def register_intake(
    intake_data: WaterIntakeCreate,
    db: Session = Depends(get_db),
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
):
    return crud_water_goal.create_intake(db, intake_data, keycloak_id)


@router.get("/intakes/", response_model=list[WaterIntakeSummary])
def list_user_intakes(
    keycloak_id: uuid.UUID = Depends(get_keycloak_id),
    db: Session = Depends(get_db),
    reference: date = None,
):
    return crud_water_goal.get_intakes_sum_week(db, keycloak_id, reference)
