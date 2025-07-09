from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.todo import ToDoCreate, ToDoRead, ToDoUpdate
from app.crud import crud_todo
from app.db.database import get_db

from app.dependencies.user import get_user_id
from app.utils.todo import get_todo_or_err


router = APIRouter()

@router.get("/", response_model=List[ToDoRead])
def read_todos(
    user_id: int = Depends(get_user_id), 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)):

    return crud_todo.get_todos(db, user_id=user_id, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model = ToDoRead)
def read_todo(
    todo_id: int, 
    user_id = Depends(get_user_id), 
    db: Session = Depends(get_db)):
   
   todo = get_todo_or_err(db, todo_id, user_id)
   return todo

@router.post("/", response_model=ToDoRead, status_code=201)
def create_todo(
    todo: ToDoCreate, 
    user_id: int = Depends(get_user_id), 
    db: Session = Depends(get_db)):

    try:
        return crud_todo.create_todo(db, todo, user_id) 
    except SQLAlchemyError as err:
        db.rollback()
        print(f"[ERRO] Erro ao criar TODO: {err}")
        raise

@router.patch("/{todo_id}", response_model=ToDoRead)
def update_todo(
    todo_id: int, 
    todo_data: ToDoUpdate, 
    user_id: int = Depends(get_user_id), 
    db: Session = Depends(get_db)):

    get_todo_or_err(db, todo_id, user_id)
    todo = crud_todo.update_todo(db, todo_id, todo_data)
    return todo

@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, user_id: int = Depends(get_user_id), db: Session = Depends(get_db)):
    get_todo_or_err(db, todo_id, user_id)
    todo = crud_todo.delete_todo(db, todo_id)

@router.patch("/{todo_id}/done-toggle", response_model=ToDoRead)
def toggle_mark(
    todo_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_user_id)
):
    todo = get_todo_or_err(db, todo_id, user_id)
    todo.done = not todo.done
    db.commit()
    db.refresh(todo)
    return todo