from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.crud import crud_water_bottle
from app.models.waterGoal import WaterBottle
from app.schemas.waterGoal import WaterBottleCreate, WaterBottleUpdate

user1 = uuid4()


def test_get_water_bottle():
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    fake_bottle = WaterBottle(
        water_bottle_id=1, bottle_name="Garrafa Azul", ml_bottle=500, keycloak_id=user1
    )
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
        WaterBottle(
            water_bottle_id=1, bottle_name="Azul", ml_bottle=500, keycloak_id=user1
        ),
        WaterBottle(
            water_bottle_id=2, bottle_name="Vermelha", ml_bottle=700, keycloak_id=user1
        ),
    ]
    mock_query.all.return_value = fake_bottles

    result = crud_water_bottle.get_water_bottle_user(mock_db, 1)

    mock_db.query.assert_called_once_with(WaterBottle)
    mock_query.filter.assert_called_once()
    assert result == fake_bottles


def test_create_water_bottle_success():
    mock_db = MagicMock()
    mock_goal = MagicMock()
    mock_goal.water_goal_id = 10

    mock_db.query.return_value.filter.return_value.first.return_value = mock_goal

    bottle_data = WaterBottleCreate(
        bottle_name="Garrafa Azul", ml_bottle=500, id_bottle_style=2
    )

    result = crud_water_bottle.create_water_bottle(
        mock_db, bottle_data, keycloak_id=user1
    )

    assert result.keycloak_id == user1
    assert result.water_goal_id == 10
    assert result.bottle_name == "Garrafa Azul"
    assert result.ml_bottle == 500
    assert result.id_bottle_style == 2

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_create_water_bottle_no_goal():
    mock_db = MagicMock()

    mock_db.query().filter().first.return_value = None

    bottle_data = WaterBottleCreate(
        bottle_name="Garrafa Azul", ml_bottle=500, id_bottle_style=2
    )

    with pytest.raises(HTTPException) as exc:
        crud_water_bottle.create_water_bottle(mock_db, bottle_data, keycloak_id=user1)

    assert exc.value.status_code == 400


def test_update_water_bottle_found():
    mock_db = MagicMock()
    fake_bottle = WaterBottle(
        water_bottle_id=1,
        bottle_name="Antiga",
        ml_bottle=400,
        keycloak_id=user1,
        id_bottle_style=1,
    )
    with patch("app.crud.crud_water_bottle.get_water_bottle", return_value=fake_bottle):
        update_data = WaterBottleUpdate(
            bottle_name="Nova", ml_bottle=600, id_bottle_style=2
        )

        result = crud_water_bottle.update_water_bottle(mock_db, 1, update_data)

        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(fake_bottle)
        assert result.bottle_name == "Nova"
        assert result.ml_bottle == 600
        assert result.id_bottle_style == 2


def test_update_water_bottle_not_found():
    mock_db = MagicMock()
    with patch("app.crud.crud_water_bottle.get_water_bottle", return_value=None):
        update_data = WaterBottleUpdate(
            bottle_name="Nova", ml_bottle=600, id_bottle_style=2
        )
        result = crud_water_bottle.update_water_bottle(mock_db, 99, update_data)

        mock_db.commit.assert_not_called()
        assert result is None


def test_delete_water_bottle_found():
    mock_db = MagicMock()
    fake_bottle = WaterBottle(
        water_bottle_id=1, bottle_name="Azul", ml_bottle=500, keycloak_id=user1
    )

    with patch("app.crud.crud_water_bottle.get_water_bottle", return_value=fake_bottle):
        result = crud_water_bottle.delete_water_bottle(mock_db, 1)

        mock_db.delete.assert_called_once_with(fake_bottle)
        mock_db.commit.assert_called_once()
        assert result == fake_bottle


def test_delete_water_bottle_not_found():
    mock_db = MagicMock()

    with patch("app.crud.crud_water_bottle.get_water_bottle", return_value=None):
        result = crud_water_bottle.delete_water_bottle(mock_db, 1)

        mock_db.delete.assert_not_called()
        mock_db.commit.assert_not_called()
        assert result is None
