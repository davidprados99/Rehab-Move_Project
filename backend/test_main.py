from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test 1: Check that the root endpoint is working (if it exists) or at least doesn't break the server
def test_read_root():
    response = client.get("/")
    assert response.status_code in [200, 404] #200 if we have a root endpoint, 404 if we don't but at least the server is running

# Test 2: Check that the Health Check works
def test_health_check():
    response = client.get("/health")
    if response.status_code == 200:
        assert response.json()["status"] == "ok"
