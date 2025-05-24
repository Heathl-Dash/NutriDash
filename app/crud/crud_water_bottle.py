from sqlalchemy.orm import Session
from app.models.waterGoal import WaterBottle

from app.schemas.waterGoal import WaterBottleCreate, WaterBottleRead, WaterBottleUpdate

def get_water_bottle(db: Session, water_bottle_id: int):
  return db.query(WaterBottle).filter(WaterBottle.water_bottle_id == water_bottle_id).first()

def get_water_bottle_user(db: Session, user_id: int):
  return db.query(WaterBottle).filter(WaterBottle.user_id == user_id).all()

def create_water_bottle(db: Session, water_bottle: WaterBottleCreate):
  db_water_bottle = WaterBottle(**water_bottle.model_dump())
  db.add(db_water_bottle)
  db.commit()
  db.refresh(db_water_bottle)
  return db_water_bottle

def update_water_bottle(db: Session, water_bottle_id: int, water_bottle_data: WaterBottleUpdate):
  db_water_bottle = get_water_bottle(db, water_bottle_id)
  if not db_water_bottle:
    return None
  for key, value in water_bottle_data.dict(exclude_unset=True).items():
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