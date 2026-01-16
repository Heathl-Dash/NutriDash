from datetime import datetime, time, timedelta

from sqlalchemy.orm import Session

from app.models.todo import ToDo, ToDohistory
from app.schemas.todo import ToDoCreate, ToDoUpdate

import uuid

def get_todo(db: Session, todo_id: int):
    return db.query(ToDo).filter(ToDo.id == todo_id).first()


def get_todos(db: Session, keycloak_id: uuid.UUID, skip: int = 0, limit: int = 100):
    return (
        db.query(ToDo)
        .filter(ToDo.keycloak_id == keycloak_id)
        .order_by(ToDo.done.asc(), ToDo.created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_todo(db: Session, todo: ToDoCreate, keycloak_id: uuid.UUID):
    db_todo = ToDo(**todo.model_dump(), keycloak_id=keycloak_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo_data: ToDoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    for key, value in todo_data.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo


def get_today_entry(db: Session, todo_id: int):
    today = datetime.combine(datetime.today().date(), time.min)
    tomorrow = today + timedelta(days=1)

    return (
        db.query(ToDohistory)
        .filter(
            ToDohistory.todo_id == todo_id,
            ToDohistory.date_done >= today,
            ToDohistory.date_done < tomorrow,
        )
        .first()
    )


def create_history(db: Session, todo_id: int, keycloak_id: uuid.UUID, date_done: datetime = None):
    if date_done is None:
        date_done = datetime.now()
    entry = ToDohistory(todo_id=todo_id, keycloak_id=keycloak_id, date_done=date_done)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def delete_history(db: Session, todo_id: int):
    entry = get_today_entry(db, todo_id)
    if entry:
        db.delete(entry)
        db.commit()
    return entry


def list_by_todo(db: Session, todo_id: int):
    return db.query(ToDohistory).filter(ToDohistory.todo_id == todo_id).all()


def list_by_user(db: Session, keycloak_id: uuid.UUID):
    return db.query(ToDohistory).filter(ToDohistory.keycloak_id == keycloak_id).all()
