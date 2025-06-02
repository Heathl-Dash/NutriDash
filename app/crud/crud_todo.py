from sqlalchemy.orm import Session
from app.models.todo import ToDo
from app.schemas.todo import ToDoCreate, ToDoUpdate

def get_todo(db: Session, todo_id:int):
    return db.query(ToDo).filter(ToDo.todo_id == todo_id).first()

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(ToDo).filter(ToDo.user_id == user_id).order_by(ToDo.done.asc(), ToDo.created.desc()).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: ToDoCreate, user_id: int):
    db_todo = ToDo(**todo.model_dump(), user_id=user_id)
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
    