from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.crud import crud_water_goal
from app.models.waterGoal import WaterGoal
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate

user1 = uuid4()
tz = ZoneInfo("America/Sao_Paulo")


def test_get_water_goal_today_robust():
    mock_db = MagicMock()
    now = datetime.now(tz)
    fake_goal = WaterGoal(
        keycloak_id=user1, ml_goal=2000, ml_drinked=500, last_updated=now
    )
    mock_db.query().filter().first.return_value = fake_goal

    result = crud_water_goal.get_water_goal(mock_db, user1)

    assert result == fake_goal
    assert result.ml_drinked == 500
    mock_db.commit.assert_not_called()


def test_get_water_goal_resets_exactly_on_new_day():
    mock_db = MagicMock()
    yesterday = datetime.now(tz) - timedelta(days=1)
    fake_goal = WaterGoal(
        keycloak_id=user1, ml_goal=2000, ml_drinked=1000, last_updated=yesterday
    )
    mock_db.query().filter().first.return_value = fake_goal

    result = crud_water_goal.get_water_goal(mock_db, user1)

    assert result.ml_drinked == 0
    assert result.last_updated.date() == datetime.now(tz).date()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(fake_goal)


def test_create_water_goal_calculation_logic():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None

    weight_val = 70
    expected_ml = 70 * 35  # 2450
    data = WaterGoalCreate(weight=weight_val)

    result = crud_water_goal.create_water_goal(mock_db, user1, data)

    assert result.ml_goal == expected_ml
    assert result.keycloak_id == user1
    mock_db.add.assert_called_once()


def test_create_water_goal_default_value_strictly():
    mock_db = MagicMock()
    mock_db.query().filter().first.return_value = None
    data = WaterGoalCreate(weight=None)

    result = crud_water_goal.create_water_goal(mock_db, user1, data)

    assert result.ml_goal == 2000


@patch("app.crud.crud_water_goal.get_water_goal")
@patch("app.crud.crud_water_goal.create_intake")
def test_update_water_goal_full_logic(mock_create_intake, mock_get_goal):
    mock_db = MagicMock()
    # Estado inicial
    fake_goal = WaterGoal(
        water_goal_id=1,
        keycloak_id=user1,
        ml_goal=1000,
        ml_drinked=100,
        last_updated=datetime.now(tz),
    )
    mock_get_goal.return_value = fake_goal

    new_weight = 80
    new_drinked = 1500
    expected_new_goal = 80 * 35  # 2800
    data = WaterGoalUpdate(ml_drinked=new_drinked, weight=new_weight)

    result = crud_water_goal.update_water_goal(mock_db, user1, data)

    assert result.ml_goal == expected_new_goal
    assert result.ml_drinked == new_drinked
    mock_create_intake.assert_called_once()
    mock_db.commit.assert_called_once()
