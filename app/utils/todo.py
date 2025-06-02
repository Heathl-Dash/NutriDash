from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import crud_todo


def get_todo_or_err(db: Session, todo_id: int, user_id: int):
  todo = crud_todo.get_todo(db, todo_id)

  if not todo:
    raise HTTPException(status_code=404, detail="ToDo not found")
  
  if todo.user_id != user_id:
    raise HTTPException(status_code=403, detail="Not authorized to access this ToDo")


  return todo