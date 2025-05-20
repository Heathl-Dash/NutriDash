from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.todo import ToDoCreate, ToDoRead, ToDoUpdate
from app.crud import crud_todo
from app.db.database import get_db

router = APIRouter(prefix="/todos", tags=["ToDos"])

@router.get("/", response_model=List[ToDoRead])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_todo.get_todos(db, skip=skip, limit=limit)

@router.get("/{todo_id}", response_model = ToDoRead)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud_todo.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@router.post("/", response_model=ToDoRead, status_code=201)
def create_todo(todo: ToDoCreate, db: Session = Depends(get_db)):
    try:
        return crud_todo.create_todo(db, todo)
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[ERRO] Erro ao criar TODO: {e}")
        raise

@router.patch("/{todo_id}", response_model=ToDoRead)
def update_todo(todo_id: int, todo_data: ToDoUpdate, db: Session = Depends(get_db)):
    todo = crud_todo.update_todo(db, todo_id, todo_data)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo

@router.delete("/{todo_id}", response_model=ToDoRead)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = crud_todo.delete_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")
    return todo