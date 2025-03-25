import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from models import Base, KeyValue
from database import get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///file::memory:?cache=shared"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_key_value(test_db):
    response = client.post("/kv/testkey", json={"value": "testvalue"})
    assert response.status_code == 200
    assert response.json() == {"key": "testkey", "value": "testvalue"}

def test_read_key_value(test_db):
    # First create a key
    client.post("/kv/testkey", json={"value": "testvalue"})
    # Then read it
    response = client.get("/kv/testkey")
    assert response.status_code == 200
    assert response.json() == {"key": "testkey", "value": "testvalue"}

def test_list_keys(test_db):
    # Create multiple keys
    client.post("/kv/key1", json={"value": "value1"})
    client.post("/kv/key2", json={"value": "value2"})
    response = client.get("/kv/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert {"key": "key1", "value": "value1"} in response.json()
    assert {"key": "key2", "value": "value2"} in response.json()

def test_delete_key(test_db):
    # First create a key
    client.post("/kv/testkey", json={"value": "testvalue"})
    # Then delete it
    response = client.delete("/kv/testkey")
    assert response.status_code == 200
    # Verify it's deleted
    response = client.get("/kv/testkey")
    assert response.status_code == 404

def test_update_key(test_db):
    # First create a key
    client.post("/kv/testkey", json={"value": "value1"})
    # Then update it
    response = client.post("/kv/testkey", json={"value": "value2"})
    assert response.status_code == 200
    assert response.json() == {"key": "testkey", "value": "value2"}

def test_key_not_found(test_db):
    response = client.get("/kv/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Key not found"} 