from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """
    Simple test to verify that the health check endpoint works.
    This acts as a basic CI test to ensure the server can start and respond.
    """
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
