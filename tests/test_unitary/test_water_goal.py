import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from fastapi import HTTPException

from app.crud import crud_water_goal 
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate
from app.models.waterGoal import WaterGoal

from uuid import uuid4

user1 = uuid4()
user2 = uuid4()

def test_get_water_goal_today():
  mock_db = MagicMock()
  now = datetime.now(ZoneInfo("America/Sao_Paulo"))

  fake_goal = WaterGoal(
    keycloak_id=user1, ml_goal=2000, ml_drinked=500, last_updated=now
  )
  mock_db.query().filter().first.return_value = fake_goal

  result = crud_water_goal.get_water_goal(mock_db, 1)

  assert result == fake_goal
  mock_db.commit.assert_not_called()


def test_get_water_goal_resets_on_new_day():
  mock_db = MagicMock()
  yesterday = datetime.now(ZoneInfo("America/Sao_Paulo")) - timedelta(days=1)

  fake_goal = WaterGoal(
      keycloak_id=1, ml_goal=2000, ml_drinked=1000, last_updated=yesterday
  )
  mock_db.query().filter().first.return_value = fake_goal

  result = crud_water_goal.get_water_goal(mock_db, user1)

  assert result.ml_drinked == 0
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once_with(fake_goal)

def test_get_water_goal_none():
  mock_db = MagicMock()
  mock_db.query().filter().first.return_value = None

  result = crud_water_goal.get_water_goal(mock_db, user1)
  assert result is None


def test_create_water_goal_success():
  mock_db = MagicMock()
  mock_db.query().filter().first.return_value = None
  data = WaterGoalCreate(weight=70)

  result = crud_water_goal.create_water_goal(mock_db, user2, data)
  
  assert result.ml_goal == 2450  
  assert isinstance(result, WaterGoal)
  mock_db.add.assert_called_once()
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once()
  

def test_create_water_goal_default_value():
  mock_db = MagicMock()
  mock_db.query().filter().first.return_value = None
  data = WaterGoalCreate(weight=None)

  result = crud_water_goal.create_water_goal(mock_db, user2, data)

  assert result.ml_goal == 2000

@patch("app.crud.crud_water_goal.get_water_goal")
def test_create_water_goal_already_exists(mock_get_goal):
  mock_db = MagicMock()
  mock_get_goal.return_value = WaterGoal(keycloak_id=user1)
  data = WaterGoalCreate(weight=60)

  with pytest.raises(HTTPException) as exc:
    crud_water_goal.create_water_goal(mock_db, user1, data)

  assert exc.value.status_code == 400

@patch("app.crud.crud_water_goal.get_water_goal")
@patch("app.crud.crud_water_goal.create_intake")
def test_update_water_goal_success(mock_create_intake, mock_get_goal):
  mock_db = MagicMock()
  fake_goal = WaterGoal(
    water_goal_id=1,
    keycloak_id=user1,
    ml_goal=2000,
    ml_drinked=500,
    last_updated=datetime.now(),
  )
  mock_get_goal.return_value = fake_goal

  data = WaterGoalUpdate(ml_drinked=800, weight=70)

  result = crud_water_goal.update_water_goal(mock_db, user1, data)

  assert result.ml_goal == round(70 * 35)
  assert result.ml_drinked == 800
  mock_create_intake.assert_called_once()
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once_with(fake_goal)


@patch("app.crud.crud_water_goal.get_water_goal", return_value=None)
def test_update_water_goal_not_found(mock_get):
  mock_db = MagicMock()
  result = crud_water_goal.update_water_goal(mock_db, user1, WaterGoalUpdate())
  assert result is None


@patch("app.crud.crud_water_goal.get_water_goal")
def test_delete_water_goal_success(mock_get):
  mock_db = MagicMock()
  fake_goal = WaterGoal(keycloak_id=user1)
  mock_get.return_value = fake_goal

  result = crud_water_goal.delete_water_goal(mock_db, user1)
  mock_db.delete.assert_called_once_with(fake_goal)
  mock_db.commit.assert_called_once()

  assert result == fake_goal

@patch("app.crud.crud_water_goal.get_water_goal", return_value=None)
def test_delete_water_goal_not_found(mock_get):
  mock_db = MagicMock()
  
  result = crud_water_goal.delete_water_goal(mock_db, user1)

  mock_db.delete.assert_not_called()

  assert result is None