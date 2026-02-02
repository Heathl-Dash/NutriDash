import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.waterGoal import WaterBottle, WaterGoal
from app.schemas.waterGoal import WaterBottleCreate, WaterBottleUpdate


def get_water_bottle(db: Session, water_bottle_id: int):
    return (
        db.query(WaterBottle)
        .filter(WaterBottle.water_bottle_id == water_bottle_id)
        .first()
    )


def get_water_bottle_user(db: Session, keycloak_id: uuid.UUID):
    return db.query(WaterBottle).filter(WaterBottle.keycloak_id == keycloak_id).all()


def create_water_bottle(
    db: Session, water_bottle: WaterBottleCreate, keycloak_id: uuid.UUID
):
    user_goal = db.query(WaterGoal).filter(WaterGoal.keycloak_id == keycloak_id).first()
    if not user_goal:
        raise HTTPException(status_code=400, detail="Water goal not found for user")

    db_water_bottle = WaterBottle(
        **water_bottle.model_dump(),
        keycloak_id=keycloak_id,
        water_goal_id=user_goal.water_goal_id,
    )
    db.add(db_water_bottle)
    db.commit()
    db.refresh(db_water_bottle)
    return db_water_bottle


def update_water_bottle(
    db: Session, water_bottle_id: int, water_bottle_data: WaterBottleUpdate
):
    db_water_bottle = get_water_bottle(db, water_bottle_id)
    if not db_water_bottle:
        return None
    for key, value in water_bottle_data.model_dump(exclude_unset=True).items():
        setattr(db_water_bottle, key, value)
    db.commit()
    db.refresh(db_water_bottle)
    return db_water_bottle


def delete_water_bottle(db: Session, water_bottle_id):
    db_water_bottle = get_water_bottle(db, water_bottle_id)
    if not db_water_bottle:
        return None
    db.delete(db_water_bottle)
    db.commit()
    return db_water_bottle
