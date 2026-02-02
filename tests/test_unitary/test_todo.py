from datetime import datetime, timedelta
from unittest.mock import MagicMock
from uuid import uuid4

from app.crud import crud_todo
from app.models.todo import ToDo
from app.schemas.todo import ToDoCreate, ToDoUpdate

user1 = uuid4()


def test_create_todo():
    mock_db = MagicMock()
    todo_data = ToDoCreate(title="ir na nutricionista na sexta", description="")
    result = crud_todo.create_todo(mock_db, todo_data, keycloak_id=user1)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.keycloak_id == user1
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
        ToDo(
            id=1,
            title="Antigo a fazer",
            done=False,
            created=now - timedelta(days=3),
            keycloak_id=user1,
        ),
        ToDo(id=2, title="Recente feito", done=True, created=now, keycloak_id=user1),
        ToDo(
            id=3,
            title="Recente a fazer",
            done=False,
            created=now - timedelta(hours=1),
            keycloak_id=user1,
        ),
    ]
    mock_query.all.return_value = fake_todos

    result = crud_todo.get_todos(mock_db, keycloak_id=user1)

    mock_db.query.assert_called_once_with(ToDo)
    mock_query.filter.assert_called_once()
    mock_query.order_by.assert_called_once()
    assert result == fake_todos


def test_update_todo():
    mock_db = MagicMock()
    fake_todo = ToDo(
        title="ir na nutricionista na sexta", description="", keycloak_id=user1
    )
    mock_db.query().filter().first.return_value = fake_todo
    mock_db.refresh = MagicMock()

    todo_update = ToDoUpdate(title="ir na nutricionista", description="sexta")

    result = crud_todo.update_todo(mock_db, 1, todo_update)

    mock_db.commit.assert_called_once()
    assert result.title == "ir na nutricionista"
    assert result.description == "sexta"


def test_delete_todo():
    mock_db = MagicMock()
    fake_todo = ToDo(id=1, title="Teste", description="Desc", keycloak_id=user1)
    mock_db.query().filter().first.return_value = fake_todo

    result = crud_todo.delete_todo(mock_db, 1)

    mock_db.delete.assert_called_once_with(fake_todo)
    mock_db.commit.assert_called_once()

    assert result == fake_todo
