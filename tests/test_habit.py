import pytest
from unittest.mock import MagicMock
from app.crud import crud_habits
from app.schemas.habits import HabitCreate, HabitUpdate
from fastapi import HTTPException


def test_create_habit():
  mock_db = MagicMock()
  habit_data = HabitCreate(title="Comer fruta", positive=True, negative = False)
  result = crud_habits.create_habit(mock_db, habit_data, keycloak_id=1)

  mock_db.add.assert_called_once()
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once()

  assert result.user_id == 1
  assert result.title == "Comer fruta"
  assert result.positive == True
  assert result.negative == False

def test_create_habit_cannot_be_both_non_positive_and_non_negative():
  mock_db = MagicMock()
  invalid_habit = HabitCreate(title="Dormir cedo", description="", positive=False, negative=False)

  with pytest.raises(HTTPException) as exc:
    crud_habits.create_habit(mock_db, invalid_habit, keycloak_id=1)

  assert exc.value.status_code == 400
  

def test_update_habit():
  mock_db = MagicMock()
  habit_data = HabitCreate(title="Comer fruta", description="", positive=True, negative = False)
  mock_db.query().filter().first.return_value = habit_data

  habit_update = HabitUpdate(description="desc", negative=True)
  result = crud_habits.update_habit(mock_db, 1, habit_update)

  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once()

  assert result.title == "Comer fruta"
  assert result.description == "desc"
  assert result.positive == True
  assert result.negative == True

def test_update_habit_cannot_be_both_non_positive_and_non_negative():
  mock_db = MagicMock()
  habit_data = HabitCreate(title="Comer fruta", description="", positive=True, negative = False)
  mock_db.query().filter().first.return_value = habit_data

  invalid_update = HabitUpdate(positive=False, negative=False)

  with pytest.raises(HTTPException) as exc:
    crud_habits.update_habit(mock_db, 1, habit_data=invalid_update)

  assert exc.value.status_code == 400


def test_delete_habit():
  mock_db = MagicMock()
  habit_data = HabitCreate(title="Comer fruta", description="", positive=True, negative = False)
  mock_db.query().filter().first.return_value = habit_data

  result = crud_habits.delete_habit(mock_db, 1)

  mock_db.delete.assert_called_once_with(habit_data)
  mock_db.commit.assert_called_once()

  assert result == habit_data 


