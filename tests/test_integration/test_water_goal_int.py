from uuid import uuid4

from app.dependencies.user import get_keycloak_id
from app.main import app
from app.schemas.waterGoal import WaterGoalCreate, WaterGoalUpdate

url = "/api/v1/nutri/water_goal/"
user1 = uuid4()


def test_read_water_goal_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate()
    client.post(url, json=data.model_dump())

    response = client.get(url)

    app.dependency_overrides.clear()

    assert response.status_code == 201


def test_create_water_goal_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate()
    response = client.post(url, json=data.model_dump())

    app.dependency_overrides.clear()

    assert response.status_code == 201


def test_delete_water_goal_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate()
    client.post(url, json=data.model_dump())

    response = client.delete(url)

    app.dependency_overrides.clear()

    assert response.status_code == 204


def test_update_water_goal_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate(ml_drinked=0, weight=93)
    client.post(url, json=data.model_dump())

    update = WaterGoalUpdate(ml_goal=4000, ml_drinked=200, weight=93)

    response = client.patch(url, json=update.model_dump())

    app.dependency_overrides.clear()

    assert response.status_code == 201


def test_read_water_goal_intakes_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate(ml_drinked=0, weight=93)
    create = client.post(url, json=data.model_dump())

    id = create.json()["water_goal_id"]

    client.post(f"{url}intakes/", json={"water_goal_id": id, "ml": 200})

    response = client.get(f"{url}intakes/")

    assert response.status_code == 200


def test_create_water_goal_intakes_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1

    data = WaterGoalCreate(ml_drinked=0, weight=93)
    create = client.post(url, json=data.model_dump())

    id = create.json()["water_goal_id"]

    response = client.post(f"{url}intakes/", json={"water_goal_id": id, "ml": 200})

    assert response.status_code == 200


def test_read_water_bottle_unauthenticated(client):
    response = client.get(url)

    assert response.status_code == 401


def test_post_water_bottle_unauthenticated(client):
    response = client.post(url)

    assert response.status_code == 401


def test_delete_water_bottle_unauthenticated(client):
    response = client.delete(url)

    assert response.status_code == 401


def test_update_water_bottle_unauthenticated(client):
    response = client.patch(url)

    assert response.status_code == 401
