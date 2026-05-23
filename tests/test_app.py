import os
import pytest

# Forzamos un archivo físico temporal antes de importar la app
os.environ["DB_PATH"] = "test_tasks.db"

from src.app import app, init_db  # noqa: E402


@pytest.fixture(autouse=True)
def setup_database():
    """Asegura que cada test use una base de datos limpia desde el archivo."""
    init_db()
    yield
    # Al terminar los tests, limpiamos el archivo para no dejar basura
    if os.path.exists("test_tasks.db"):
        try:
            os.remove("test_tasks.db")
        except PermissionError:
            pass  # Si Windows retiene el archivo, lo ignora


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as test_client:
        yield test_client


# ==========================================
# TUS 5 TESTS
# ==========================================


def test_get_index(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "To-Do API"


def test_list_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    response = client.post('/tasks', json={"title": "Test DevOps"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Test DevOps"


def test_create_task_invalid(client):
    response = client.post('/tasks', json={})
    assert response.status_code == 400


def test_task_lifecycle(client):
    res = client.post('/tasks', json={"title": "Ciclo"})
    t_id = res.get_json()["id"]

    assert client.get(f'/tasks/{t_id}').status_code == 200
    assert client.put(f'/tasks/{t_id}', json={"completed": 1}).status_code == 200
    assert client.delete(f'/tasks/{t_id}').status_code == 200
    assert client.get(f'/tasks/{t_id}').status_code == 404