import pytest
from unittest.mock import MagicMock, patch
from app.crud import crud_todo
from app.schemas.todo import ToDoCreate, ToDoUpdate
from app.models.todo import ToDo, ToDohistory
from datetime import datetime, timedelta


def test_get_todo_returns_todo():
  mock_db = MagicMock()
  fake_todo = MagicMock()
  mock_db.query().filter().first.return_value = fake_todo

  result = crud_todo.get_todo(mock_db, 1)

  mock_db.query.assert_called()
  mock_db.query().filter.assert_called()
  assert result == fake_todo


def test_get_todo_returns_none_when_not_found():
  mock_db = MagicMock()
  mock_db.query().filter().first.return_value = None

  result = crud_todo.get_todo(mock_db, 999)
  assert result is None


def test_create_todo():
  mock_db = MagicMock()
  todo_data = ToDoCreate(title="ir na nutricionista na sexta")
  result = crud_todo.create_todo(mock_db, todo_data, user_id=1)

  mock_db.add.assert_called()
  mock_db.commit.assert_called()
  mock_db.refresh.assert_called()

  assert result.user_id == 1
  assert result.title == "ir na nutricionista na sexta"

def test_get_todos_returns_sorted_results():
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query

    now = datetime.now()
    fake_todos = [
        ToDo(id=1, title="Antigo a fazer", done=False, created=now - timedelta(days=3), user_id=1),
        ToDo(id=2, title="Recente feito", done=True, created=now, user_id=1),
        ToDo(id=3, title="Recente a fazer", done=False, created=now - timedelta(hours=1), user_id=1),
    ]
    mock_query.all.return_value = fake_todos

    result = crud_todo.get_todos(mock_db, user_id=1)

    mock_db.query.assert_called_with(ToDo)
    mock_query.filter.assert_called()
    mock_query.order_by.assert_called()
    assert result == fake_todos

def test_update_todo():
  mock_db = MagicMock()
  fake_todo = ToDo(title="ir na nutricionista na sexta", description="", user_id=1)
  mock_db.query().filter().first.return_value = fake_todo
  mock_db.refresh = MagicMock()

  todo_update = ToDoUpdate(title="ir na nutricionista", description="sexta")

  result = crud_todo.update_todo(mock_db, 1, todo_update)

  mock_db.commit.assert_called()
  assert result.title == "ir na nutricionista"
  assert result.description == "sexta"

def test_update_todo_returns_none_if_not_found():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None
    todo_update = MagicMock()

    result = crud_todo.update_todo(mock_db, 999, todo_update)

    assert result is None
    mock_db.commit.assert_not_called()

def test_delete_todo():
    mock_db = MagicMock()
    fake_todo = ToDo(id=1, title="Teste", description="Desc", user_id=1)
    mock_db.query().filter().first.return_value = fake_todo

    result = crud_todo.delete_todo(mock_db, 1)

    mock_db.delete.assert_called_with(fake_todo)
    mock_db.commit.assert_called()

    assert result == fake_todo

def test_delete_todo_returns_none_if_not_found():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    result = crud_todo.delete_todo(mock_db, 999)

    assert result is None
    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()


def test_get_today_entry_found():
    mock_db = MagicMock()
    fake_entry = ToDohistory(todo_id=1, user_id=1)
    mock_db.query().filter().first.return_value = fake_entry

    result = crud_todo.get_today_entry(mock_db, 1)

    mock_db.query.assert_called_with(ToDohistory)
    mock_db.query().filter.assert_called()
    assert result == fake_entry


def test_get_today_entry_not_found():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    result = crud_todo.get_today_entry(mock_db, 1)
    assert result is None


def test_create_history_with_default_date():
    mock_db = MagicMock()
    fake_now = datetime(2025, 10, 17, 12, 0, 0)

    with patch("app.crud.crud_todo.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        result = crud_todo.create_history(mock_db, todo_id=1, user_id=1)

    mock_db.add.assert_called()
    mock_db.commit.assert_called()
    mock_db.refresh.assert_called()
    assert result.todo_id == 1
    assert result.user_id == 1
    assert isinstance(result.date_done, datetime)


def test_delete_history_found():
    mock_db = MagicMock()
    fake_entry = ToDohistory(todo_id=1, user_id=1)
    mock_db.query().filter().first.return_value = fake_entry

    result = crud_todo.delete_history(mock_db, todo_id=1)

    mock_db.delete.assert_called_with(fake_entry)
    mock_db.commit.assert_called()
    assert result == fake_entry


def test_delete_history_not_found():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    result = crud_todo.delete_history(mock_db, todo_id=1)

    mock_db.delete.assert_not_called()
    mock_db.commit.assert_not_called()
    assert result is None


def test_list_by_todo_returns_history():
    mock_db = MagicMock()
    fake_history = [ToDohistory(todo_id=1, user_id=1)]
    mock_db.query().filter().all.return_value = fake_history

    result = crud_todo.list_by_todo(mock_db, todo_id=1)

    mock_db.query.assert_called_with(ToDohistory)
    mock_db.query().filter.assert_called()
    assert result == fake_history

def test_list_by_user_returns_history():
    mock_db = MagicMock()
    fake_history = [
        ToDohistory(todo_id=1, user_id=1),
        ToDohistory(todo_id=2, user_id=1),
    ]
    mock_db.query().filter().all.return_value = fake_history

    result = crud_todo.list_by_user(mock_db, user_id=1)

    mock_db.query.assert_called_with(ToDohistory)
    mock_db.query().filter.assert_called()
    assert result == fake_history

