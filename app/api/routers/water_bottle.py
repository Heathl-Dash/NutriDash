from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.waterGoal import WaterBottleCreate, WaterBottleRead, WaterBottleUpdate
from app.crud import crud_water_bottle
from app.db.database import get_db

from app.dependencies.user import get_user_id
from app.utils.water_bottle import get_water_bottle_or_err

router = APIRouter(prefix="/water_bottle", tags=["WaterBottle"])

@router.get("/list", response_model=List[WaterBottleRead], status_code=200)
def read_water_bottles(user_id: int = Depends(get_user_id),db: Session = Depends(get_db)):
    return crud_water_bottle.get_water_bottle_user(db, user_id=user_id)

@router.get("/{water_bottle_id}", response_model=WaterBottleRead, status_code=200)
def read_water_bottle(water_bottle_id: int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    water_bottle = get_water_bottle_or_err(db,water_bottle_id, user_id)
    return water_bottle

@router.post("/", response_model=WaterBottleRead, status_code=201)
def create_water_bottle(water_bottle: WaterBottleCreate, user_id: int = Depends(get_user_id),db: Session = Depends(get_db)):
    try:
      return crud_water_bottle.create_water_bottle(db, water_bottle, user_id)
    except SQLAlchemyError as err:
      db.rollback()
      print(f"[ERRO] Erro ao criar WATER BOTTLE: {err}")
      raise

@router.patch("/{water_bottle_id}", response_model=WaterBottleRead, status_code=201)
def update_water_bottle(water_bottle_id: int, water_bottle_data:WaterBottleUpdate, user_id: int = Depends(get_user_id), db:Session = Depends(get_db)):
  get_water_bottle_or_err(db, water_bottle_id, user_id)
  water_bottle = crud_water_bottle.update_water_bottle(db, water_bottle_id, water_bottle_data)
  if not water_bottle:
    raise HTTPException(status_code=404, detail="Water bottle not found")
  return water_bottle


@router.delete("/{water_bottle_id}", status_code=204)
def delete_water_bottle(water_bottle_id:int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
  get_water_bottle_or_err(db, water_bottle_id, user_id)
  return crud_water_bottle.delete_water_bottle(db, water_bottle_id)