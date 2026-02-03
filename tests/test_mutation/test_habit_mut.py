from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.crud import crud_habits
from app.schemas.habits import HabitCreate, HabitUpdate

user1 = uuid4()


def test_create_habit():
    mock_db = MagicMock()
    habit_data = HabitCreate(
        title="Comer fruta", description="Diário", positive=True, negative=False
    )

    result = crud_habits.create_habit(mock_db, habit_data, keycloak_id=user1)

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

    assert result.keycloak_id == user1
    assert result.title == "Comer fruta"
    assert result.description == "Diário"
    assert result.positive is True
    assert result.negative is False


def test_create_habit_validation_logic():
    mock_db = MagicMock()
    invalid_habit = HabitCreate(
        title="Erro", description="", positive=False, negative=False
    )

    with pytest.raises(HTTPException) as exc:
        crud_habits.create_habit(mock_db, invalid_habit, keycloak_id=user1)

    assert exc.value.status_code == 400


def test_update_habit_comprehensive():
    mock_db = MagicMock()

    existing_habit = MagicMock()
    existing_habit.title = "Antigo"
    existing_habit.description = "Antiga"
    existing_habit.positive = True
    existing_habit.negative = False

    mock_db.query().filter().first.return_value = existing_habit

    update_data = HabitUpdate(
        title="Novo Titulo", description="Nova Desc", positive=False, negative=True
    )

    result = crud_habits.update_habit(mock_db, 1, update_data)

    mock_db.commit.assert_called_once()

    assert result.title == "Novo Titulo"
    assert result.description == "Nova Desc"
    assert result.positive is False
    assert result.negative is True
