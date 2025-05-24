from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.waterGoal import WaterBottleCreate, WaterBottleRead, WaterBottleUpdate
from app.crud import crud_water_bottle
from app.db.database import get_db

router = APIRouter(prefix="/water_bottle", tags=["WaterBottle"])

@router.get("/{water_bottle_id}", response_model=WaterBottleRead, status_code=201)
def read_water_bottle(water_bottle_id, db: Session = Depends(get_db)):
  water_bottle = crud_water_bottle.get_water_bottle(db, water_bottle_id)
  if not water_bottle:
    raise HTTPException(status_code=404, detail="Water bottle not found")
  return water_bottle
