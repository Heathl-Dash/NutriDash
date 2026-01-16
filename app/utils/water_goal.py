from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_water_goal

import uuid

def get_water_goal_or_err(db: Session, keycloak_id: uuid.UUID):
    water_goal = crud_water_goal.get_water_goal(db, keycloak_id)

    if not water_goal:
        raise HTTPException(status_code=404, detail="water_goal not found")

    if water_goal.keycloak_id != keycloak_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this water_goal"
        )

    return water_goal
