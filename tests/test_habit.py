import pytest
from unittest.mock import MagicMock
from app.crud import crud_habits
from app.schemas.habits import HabitCreate, HabitUpdate
from fastapi import HTTPException
from app.models.habits import Habit

def test_get_habit_returns_habit():
  mock_db = MagicMock()
  fake_habit = Habit(id=1, title="Ler", description="Ler um livro", user_id=1)
  mock_db.query().filter().first.return_value = fake_habit

  result = crud_habits.get_habit(mock_db, 1)
  mock_db.query.assert_called()

  assert result == fake_habit


def test_get_habit_returns_none():
  mock_db = MagicMock()
  mock_db.query().filter().first.return_value = None

  result = crud_habits.get_habit(mock_db, 99)
  assert result is None

def test_get_habits_base_query():
  mock_db = MagicMock()
  fake_list = [Habit(id=1), Habit(id=2)]
  mock_db.query().filter().order_by().offset().limit().all.return_value = fake_list

  result = crud_habits.get_habits(mock_db, user_id=1)
  mock_db.query.assert_called()
  assert result == fake_list


def test_get_habits_positive_filter():
  mock_db = MagicMock()
  crud_habits.get_habits(mock_db, user_id=1, positive=True)
  mock_db.query().filter().filter.assert_called()


def test_get_habits_negative_filter():
  mock_db = MagicMock()
  crud_habits.get_habits(mock_db, user_id=1, negative=True)
  mock_db.query().filter().filter.assert_called()

def test_create_habit():
  mock_db = MagicMock()
  habit_data = HabitCreate(title="Comer fruta", positive=True, negative = False)
  result = crud_habits.create_habit(mock_db, habit_data, user_id=1)

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
    crud_habits.create_habit(mock_db, invalid_habit, user_id=1)

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


def test_filter_positive_habits():
    mock_db = MagicMock()
    mock_db.query().filter().all.return_value = ["habit1", "habit2"]
    result = crud_habits.filter_positive_habits(mock_db, 1)
    assert result == ["habit1", "habit2"]
    mock_db.query.assert_called()


def test_filter_negative_habits():
  mock_db = MagicMock()
  mock_db.query().filter().all.return_value = ["habit3"]
  result = crud_habits.filter_negative_habits(mock_db, 1)
  assert result == ["habit3"]
  mock_db.query.assert_called()


