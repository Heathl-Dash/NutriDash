from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_todo

import uuid

def get_todo_or_err(db: Session, todo_id: int, keycloak_id: uuid.UUID):
    todo = crud_todo.get_todo(db, todo_id)

    if not todo:
        raise HTTPException(status_code=404, detail="ToDo not found")

    if todo.keycloak_id != keycloak_id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this ToDo"
        )

    return todo
