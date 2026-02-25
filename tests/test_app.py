import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No special setup needed
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check status and response structure
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_for_activity():
    # Arrange: Choose an activity and a unique email
    activity = "Chess Club"
    email = "newstudent@example.com"
    
    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Check success response and that participant was added
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    # Verify in activities data
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity]["participants"]

def test_signup_already_signed_up():
    # Arrange: Sign up once
    activity = "Programming Class"
    email = "duplicate@example.com"
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act: Attempt to sign up again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Should fail with 400
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}

def test_signup_activity_not_found():
    # Arrange: Use a non-existent activity
    activity = "Nonexistent Activity"
    email = "test@example.com"
    
    # Act: Make POST request
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert: Should return 404
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}

def test_root_redirect():
    # Arrange: Create client that doesn't follow redirects
    client_no_redirect = TestClient(app, follow_redirects=False)
    
    # Act: GET request to root
    response = client_no_redirect.get("/")
    
    # Assert: Should redirect to static index
    assert response.status_code == 307  # Temporary redirect
    assert "/static/index.html" in response.headers["location"]