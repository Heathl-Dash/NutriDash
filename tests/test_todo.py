import pytest
from unittest.mock import MagicMock
from app.crud import crud_todo
from app.schemas.todo import ToDoCreate, ToDoUpdate
from app.models.todo import ToDo
from datetime import datetime, timedelta


def test_create_todo():
  mock_db = MagicMock()
  todo_data = ToDoCreate(title="ir na nutricionista na sexta")
  result = crud_todo.create_todo(mock_db, todo_data, user_id=1)

  mock_db.add.assert_called_once()
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once()

  assert result.user_id == 1
  assert result.title == "ir na nutricionista na sexta"


def test_update_todo():
  mock_db = MagicMock()
  fake_todo = ToDo(title="ir na nutricionista na sexta", description="", user_id=1)
  mock_db.query().filter().first.return_value = fake_todo
  mock_db.refresh = MagicMock()

  todo_update = ToDoUpdate(title="ir na nutricionista", description="sexta")

  result = crud_todo.update_todo(mock_db, 1, todo_update)

  mock_db.commit.assert_called_once()
  assert result.title == "ir na nutricionista"
  assert result.description == "sexta"

def test_delete_todo():
    mock_db = MagicMock()
    fake_todo = ToDo(id=1, title="Teste", description="Desc", user_id=1)
    mock_db.query().filter().first.return_value = fake_todo

    result = crud_todo.delete_todo(mock_db, 1)

    mock_db.delete.assert_called_once_with(fake_todo)
    mock_db.commit.assert_called_once()

    assert result == fake_todo




