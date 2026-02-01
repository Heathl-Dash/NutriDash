from uuid import uuid4

from app.main import app
from app.dependencies.user import get_keycloak_id
from app.schemas.habits import HabitCreate, HabitUpdate

user1 = uuid4()
prefix = "/api/v1/nutri/"

def test_read_habits_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    response = client.get(prefix + "habit/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_create_habits_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=False, negative=True)
    
    response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
    
    app.dependency_overrides.clear()

    assert response.status_code == 201
    
def test_delete_habit_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=False, negative=True)
    create_response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
        
    habit_id = create_response.json()["id"]
    
    response = client.delete(f"{prefix}habit/{habit_id}")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 204
    
def test_update_habit_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=False, negative=True)
    create_response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
        
    habit_id = create_response.json()["id"]
    habit_update = HabitUpdate(title="Hábito atualizado")
    
    response = client.patch(f"{prefix}habit/{habit_id}", json=habit_update.model_dump(exclude_unset=True))
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    assert response.json()["title"] == "Hábito atualizado"
    

def test_retrieve_habit_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=False, negative=True)
    create_response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
        
    habit_id = create_response.json()["id"]
    
    response = client.get(f"{prefix}habit/{habit_id}")
    
    assert response.status_code == 200 
    assert response.json()["title"] == "Novo hábito"
    
def test_add_positive_counter_habit_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=True, negative=False)
    create_response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
        
    habit_id = create_response.json()["id"]
    
    response = client.patch(f"{prefix}habit/{habit_id}/add-positive-counter")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    assert response.json()["positive_count"] == 1
    
def test_add_negative_counter_habit_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    habit_data = HabitCreate(title="Novo hábito", description="", positive=False, negative=True)
    create_response = client.post(f"{prefix}habit/", json = habit_data.model_dump())
        
    habit_id = create_response.json()["id"]
    
    response = client.patch(f"{prefix}habit/{habit_id}/add-negative-counter")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    assert response.json()["negative_count"] == 1
    
def test_read_habits_unauthenticated(client):    
    response = client.get(prefix + "habit/")
    
    assert response.status_code == 401
    
def test_post_habits_unauthenticated(client):    
    response = client.post(prefix + "habit/")
    
    assert response.status_code == 401
    
def test_delete_habits_unauthenticated(client):    
    response = client.delete(prefix + "habit/1")
    
    assert response.status_code == 401
    
def test_update_habits_unauthenticated(client):    
    response = client.patch(prefix + "habit/1")
    
    assert response.status_code == 401
    
def test_add_positive_counter_habits_unauthenticated(client):    
    response = client.patch(prefix + "habit/1/add-positive-counter")
    
    assert response.status_code == 401
    
def test_add_negative_counter_habits_unauthenticated(client):    
    response = client.patch(prefix + "habit/1/add-negative-counter")
    
    assert response.status_code == 401