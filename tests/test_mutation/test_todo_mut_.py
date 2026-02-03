from unittest.mock import MagicMock
from uuid import uuid4

from app.crud import crud_todo
from app.models.todo import ToDo
from app.schemas.todo import ToDoCreate, ToDoUpdate

user1 = uuid4()


def test_create_todo_robust():
    mock_db = MagicMock()
    todo_data = ToDoCreate(title="Título Único", description="Descrição Única")

    result = crud_todo.create_todo(mock_db, todo_data, keycloak_id=user1)

    mock_db.add.assert_called_once()
    added_obj = mock_db.add.call_args[0][0]
    assert added_obj.title == "Título Único"
    assert added_obj.keycloak_id == user1

    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_get_todos_logic_and_ordering():
    mock_db = MagicMock()

    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter.return_value
    mock_order = mock_filter.order_by.return_value
    mock_offset = mock_order.offset.return_value
    mock_limit = mock_offset.limit.return_value

    fake_todos = [ToDo(id=1, title="Teste")]
    mock_limit.all.return_value = fake_todos

    result = crud_todo.get_todos(mock_db, keycloak_id=user1, skip=5, limit=10)

    mock_db.query.assert_called_once_with(ToDo)

    mock_query.filter.assert_called_once()

    mock_filter.order_by.assert_called_once()

    mock_order.offset.assert_called_once_with(5)
    mock_offset.limit.assert_called_once_with(10)

    assert result == fake_todos


def test_update_todo_full_change():
    mock_db = MagicMock()
    fake_todo = ToDo(
        title="Antigo", description="Antiga", done=False, keycloak_id=user1
    )
    mock_db.query().filter().first.return_value = fake_todo

    # Dados de atualização mudando TUDO
    todo_update = ToDoUpdate(title="Novo", description="Nova", done=True)

    result = crud_todo.update_todo(mock_db, 1, todo_update)

    mock_db.commit.assert_called_once()
    assert result.title == "Novo"
    assert result.description == "Nova"
    assert result.done is True


def test_delete_todo_verification():
    mock_db = MagicMock()
    fake_todo = ToDo(id=99, title="Deletar", keycloak_id=user1)
    mock_db.query().filter().first.return_value = fake_todo

    result = crud_todo.delete_todo(mock_db, 99)

    mock_db.delete.assert_called_once_with(fake_todo)
    mock_db.commit.assert_called_once()
    assert result.id == 99
