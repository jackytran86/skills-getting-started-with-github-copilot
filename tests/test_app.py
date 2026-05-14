import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities to initial state before each test
    global activities
    activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interscholastic tournaments",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["jason@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and various art mediums",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["grace@mergington.edu"]
        },
        "Drama Club": {
            "Act in plays and musicals, develop performance skills",
            "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["luke@mergington.edu", "ava@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills in competitive debates",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore advanced scientific concepts",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["zoe@mergington.edu", "ethan@mergington.edu"]
        }
    }

def test_root_redirect(client):
    # Arrange: No special setup needed
    
    # Act: Make GET request to root
    response = client.get("/")
    
    # Assert: Should redirect to static/index.html
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client):
    # Arrange: Activities are set up in fixture
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Should return activities dict
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"

def test_signup_successful(client):
    # Arrange: Choose an activity and new email
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act: POST to signup endpoint
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert: Should succeed and add participant
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]

def test_signup_activity_not_found(client):
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act: POST to signup
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert: Should return 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_already_signed_up(client):
    # Arrange: Use an activity and an email already signed up
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in participants
    
    # Act: POST to signup
    response = client.post(f"/activities/{activity_name}/signup", json={"email": email})
    
    # Assert: Should return 400
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_remove_participant_successful(client):
    # Arrange: Choose an activity and existing participant
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    
    # Act: DELETE to remove participant
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Should succeed and remove participant
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]

def test_remove_participant_activity_not_found(client):
    # Arrange: Use non-existent activity
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act: DELETE to remove
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Should return 404
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant_not_signed_up(client):
    # Arrange: Use activity and email not signed up
    activity_name = "Chess Club"
    email = "notsignedup@mergington.edu"
    
    # Act: DELETE to remove
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    
    # Assert: Should return 400
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"