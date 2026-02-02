import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_water_bottle


def get_water_bottle_or_err(db: Session, water_bottle_id: int, keycloak_id: uuid.UUID):
    water_bottle = crud_water_bottle.get_water_bottle(db, water_bottle_id)

    if not water_bottle:
        raise HTTPException(status_code=404, detail="Water Bottle not found")

    if water_bottle.keycloak_id != keycloak_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this Water Bottle"
        )

    return water_bottle
