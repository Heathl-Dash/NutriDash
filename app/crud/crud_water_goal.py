from collections import defaultdict
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.waterGoal import WaterBottle, WaterGoal, WaterIntake
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate, WaterIntakeCreate


def get_water_goal(db: Session, user_id: int):
    water_goal = db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()
    if not water_goal:
        return None

    now_local = datetime.now(ZoneInfo("America/Sao_Paulo"))
    today_local = now_local.date()

    if water_goal.last_updated.date() < today_local:
        water_goal.ml_drinked = 0
        water_goal.last_updated = now_local
        db.commit()
        db.refresh(water_goal)

    return water_goal


def get_water_goal_by_user(db: Session, user_id: int):
    return db.query(WaterGoal).filter(WaterGoal.user_id == user_id).first()


def create_water_goal(db: Session, user_id: int, water_goal: WaterGoalCreate):
    has_water_goal = get_water_goal_by_user(db, user_id)
    if has_water_goal:
        raise HTTPException(
            status_code=400, detail="Water goal already exists for this user"
        )

    if water_goal.weight is not None and water_goal.weight > 0:
        daily_goal = round(water_goal.weight * 35)
    else:
        daily_goal = 2000

    data = water_goal.model_dump(exclude={"ml_goal", "weight"})

    db_water_goal = WaterGoal(**data, user_id=user_id, ml_goal=daily_goal)
    db.add(db_water_goal)
    db.commit()
    db.refresh(db_water_goal)
    return db_water_goal


def update_water_goal(db: Session, user_id: int, water_goal_data: WaterGoalUpdate):
    db_water_goal = get_water_goal(db, user_id)
    if not db_water_goal:
        return None

    if water_goal_data.weight is not None and water_goal_data.weight > 0:
        db_water_goal.ml_goal = round(water_goal_data.weight * 35)

    ml_drinked_before = db_water_goal.ml_drinked
    ml_drinked_after = water_goal_data.ml_drinked

    ml_intake = ml_drinked_after - ml_drinked_before

    for key, value in water_goal_data.model_dump(exclude_unset=True).items():
        setattr(db_water_goal, key, value)
    db.commit()
    db.refresh(db_water_goal)

    if ml_drinked_before is not None and ml_drinked_after > ml_drinked_before:
        intake_data = WaterIntakeCreate(
            water_goal_id=db_water_goal.water_goal_id, ml=ml_intake
        )
        create_intake(db, intake_data, user_id)

    return db_water_goal


def delete_water_goal(db: Session, user_id):
    db_water_goal = get_water_goal(db, user_id)
    if not db_water_goal:
        return None
    db.delete(db_water_goal)
    db.commit()
    return db_water_goal


def create_intake(db: Session, intake_data: WaterIntakeCreate, user_id: int):
    intake = WaterIntake(**intake_data.model_dump(), user_id=user_id)
    db.add(intake)
    db.commit()
    db.refresh(intake)
    return intake


def get_week_range(reference: datetime = None):
    if reference is None:
        reference = date.today()

    start = reference - timedelta(days=reference.weekday())
    end = start + timedelta(days=6)

    start = datetime.combine(start, datetime.min.time())
    end = datetime.combine(end, datetime.max.time())

    return start, end


def get_intakes_sum_week(db: Session, user_id: int, reference: date = None):
    start, end = get_week_range(reference)
    results = (
        db.query(WaterIntake)
        .filter(
            WaterIntake.user_id == user_id,
            WaterIntake.timestamp >= start,
            WaterIntake.timestamp <= end,
        )
        .all()
    )
    daily_totals = defaultdict(int)
    for entry in results:
        day = entry.timestamp.date()
        daily_totals[day] += entry.ml
    week_data = []
    for i in range(7):
        day = (start + timedelta(days=i)).date()
        week_data.append({"date": day.isoformat(), "total_ml": daily_totals[day]})
    return week_data


def get_intakes_by_user(db: Session, user_id: int):
    return db.query(WaterIntake).filter(WaterIntake.user_id == user_id).all()


def get_intakes_by_goal(db: Session, goal_id: int):
    return db.query(WaterIntake).filter(WaterIntake.water_goal_id == goal_id).all()
