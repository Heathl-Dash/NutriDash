import pytest
from unittest.mock import MagicMock, patch
from app.crud import crud_water_bottle
from app.schemas.waterGoal import WaterBottleCreate, WaterBottleUpdate
from app.models.waterGoal import WaterBottle
from fastapi import HTTPException

def test_get_water_bottle():
  mock_db = MagicMock()
  mock_query = MagicMock()
  mock_db.query.return_value = mock_query
  mock_query.filter.return_value = mock_query
  fake_bottle = WaterBottle(water_bottle_id=1, bottle_name="Garrafa Azul", ml_bottle=500, user_id=1)
  mock_query.first.return_value = fake_bottle

  result = crud_water_bottle.get_water_bottle(mock_db, 1)

  mock_db.query.assert_called_once_with(WaterBottle)
  mock_query.filter.assert_called_once()
  assert result == fake_bottle


def test_get_water_bottle_user():
  mock_db = MagicMock()
  mock_query = MagicMock()
  mock_db.query.return_value = mock_query
  mock_query.filter.return_value = mock_query
  fake_bottles = [
      WaterBottle(water_bottle_id=1, bottle_name="Azul", ml_bottle=500, user_id=1),
      WaterBottle(water_bottle_id=2, bottle_name="Vermelha", ml_bottle=700, user_id=1),
  ]
  mock_query.all.return_value = fake_bottles

  result = crud_water_bottle.get_water_bottle_user(mock_db, 1)

  mock_db.query.assert_called_once_with(WaterBottle)
  mock_query.filter.assert_called_once()
  assert result == fake_bottles


@patch("app.crud.crud_water_bottle.get_water_goal_by_user")
def test_create_water_bottle_success(mock_get_goal):
  mock_db = MagicMock()
  mock_goal = MagicMock()
  mock_goal.water_goal_id = 10
  mock_get_goal.return_value = mock_goal

  bottle_data = WaterBottleCreate(bottle_name="Garrafa Azul", ml_bottle=500, id_bottle_style=2)

  result = crud_water_bottle.create_water_bottle(mock_db, bottle_data, user_id=1)

  mock_get_goal.assert_called_once_with(mock_db, 1)
  mock_db.add.assert_called_once()
  mock_db.commit.assert_called_once()
  mock_db.refresh.assert_called_once()

  assert result.user_id == 1
  assert result.water_goal_id == 10
  assert result.bottle_name == "Garrafa Azul"
  assert result.ml_bottle == 500
  assert result.id_bottle_style == 2

@patch("app.crud.crud_water_bottle.get_water_goal_by_user")
def test_create_water_bottle_no_goal(mock_get_goal):
  mock_db = MagicMock()  
  mock_get_goal.return_value = None
  bottle_data = WaterBottleCreate(bottle_name="Garrafa Azul", ml_bottle=500, id_bottle_style=2)

  with pytest.raises(HTTPException) as exc:
    crud_water_bottle.create_water_bottle(mock_db, bottle_data, user_id=1)

  assert exc.value.status_code == 400





   


