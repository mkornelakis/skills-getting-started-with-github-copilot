import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities
def test_get_activities():
    # Arrange: (No setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

# Test POST /activities/{activity_name}/signup
def test_signup_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200 or response.status_code == 400  # 400 if already signed up

# Test POST /activities/{activity_name}/unregister
def test_unregister_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@example.com"
    # First, ensure the user is signed up
    client.post(f"/activities/{activity_name}/signup", params={"email": email})
    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 200 or response.status_code == 404  # 404 if not found

# Test error case: missing email
def test_signup_missing_email():
    # Arrange
    activity_name = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity_name}/signup")
    # Assert
    assert response.status_code == 422  # Unprocessable Entity (validation error)
