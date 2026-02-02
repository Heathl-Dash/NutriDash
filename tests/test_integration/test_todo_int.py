from uuid import uuid4

from app.dependencies.user import get_keycloak_id
from app.main import app
from app.schemas import todo
from app.schemas.todo import ToDoCreate, ToDoUpdate


user1 = uuid4()
prefix = "/api/v1/nutri/"

def test_read_todo_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    response = client.get(f"{prefix}todo/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_create_todo_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    todo_data = ToDoCreate(title="Nova tarefa", description="")
    
    response = client.post(f"{prefix}todo/", json=todo_data.model_dump())
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 201
    
def test_delete_todo_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    todo_data = ToDoCreate(title="Nova Tarefa", description="")
    create_response = client.post(f"{prefix}todo/", json = todo_data.model_dump())
        
    todo_id = create_response.json()["id"]
    
    response = client.delete(f"{prefix}todo/{todo_id}")
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 204
    
def test_update_todo_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    todo_data = ToDoCreate(title="Nova Tarefa", description="")
    create_response = client.post(f"{prefix}todo/", json = todo_data.model_dump())
        
    todo_id = create_response.json()["id"]
    todo_update = ToDoUpdate(title="Tarefa atualizado")
    
    response = client.patch(f"{prefix}todo/{todo_id}", json=todo_update.model_dump(exclude_unset=True))
    
    app.dependency_overrides.clear()
    
    assert response.status_code == 200
    assert response.json()["title"] == "Tarefa atualizado"
    
def test_retrieve_todo_authenticated(client):
    app.dependency_overrides[get_keycloak_id] = lambda: user1
    
    todo_data = ToDoCreate(title="Nova Tarefa", description="")
    create_response = client.post(f"{prefix}todo/", json = todo_data.model_dump())
        
    todo_id = create_response.json()["id"]
    
    response = client.get(f"{prefix}todo/{todo_id}")
    
    assert response.status_code == 200 
    assert response.json()["title"] == "Nova Tarefa"
    
def test_read_todos_unauthenticated(client):    
    response = client.get(prefix + "todo/")
    
    assert response.status_code == 401
    
def test_post_todos_unauthenticated(client):    
    response = client.post(prefix + "todo/")
    
    assert response.status_code == 401
    
def test_delete_todos_unauthenticated(client):    
    response = client.delete(prefix + "todo/1")
    
    assert response.status_code == 401
    
def test_update_todos_unauthenticated(client):    
    response = client.patch(prefix + "todo/1")
    
    assert response.status_code == 401