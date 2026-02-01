from uuid import uuid4

from app.dependencies.user import get_keycloak_id
from app.main import app
from app.schemas.waterGoal import WaterBottleCreate, WaterBottleUpdate, WaterGoalCreate 


url = "/api/v1/nutri/water_bottle/"
user1 = uuid4()

def test_read_water_bottle_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    response = client.get(url)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_create_water_bottle_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    water_goal = WaterGoalCreate()
    
    client.post("/api/v1/nutri/water_goal/", json=water_goal.model_dump())
        
    water_bottle_data = WaterBottleCreate(
        bottle_name="Nova garrafa", 
        ml_bottle=2000, 
        id_bottle_style=2
    )
    
    response = client.post(url, json=water_bottle_data.model_dump())
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 201

def test_delete_water_bottle_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    water_goal = WaterGoalCreate()
    
    client.post("/api/v1/nutri/water_goal/", json=water_goal.model_dump())
    
    water_bottle_data = WaterBottleCreate(
        bottle_name="Nova garrafa", 
        ml_bottle=2000, 
        id_bottle_style=2
    )
    
    bottle_create = client.post(url, json=water_bottle_data.model_dump())
    
    bottle_id = bottle_create.json()['water_bottle_id']
    
    response = client.delete(f"{url}{bottle_id}")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 204
    
def test_update_water_bottle_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    water_goal = WaterGoalCreate()
    
    client.post("/api/v1/nutri/water_goal/", json=water_goal.model_dump())
    
    water_bottle_data = WaterBottleCreate(
        bottle_name="Nova garrafa", 
        ml_bottle=2000, 
        id_bottle_style=2
    )
    
    bottle_create = client.post(url, json=water_bottle_data.model_dump())
    
    bottle_id = bottle_create.json()['water_bottle_id']
    
    update = WaterBottleUpdate(id_bottle_style=3)
    
    response = client.patch(f"{url}{bottle_id}", json=update.model_dump(exclude_unset=True))
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 201
    

    

    
        
    
    
