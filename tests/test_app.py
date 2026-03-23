import copy

import pytest
from fastapi.testclient import TestClient

from app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset in-memory activities state before each test."""
    original = {
        name: copy.deepcopy(data)
        for name, data in {
            "Chess Club": {
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            "Programming Class": {
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            "Gym Class": {
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
            "Basketball Team": {
                "description": "Competitive basketball league and training",
                "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
                "max_participants": 15,
                "participants": ["alex@mergington.edu"],
            },
            "Tennis Club": {
                "description": "Learn tennis skills and participate in matches",
                "schedule": "Saturdays, 10:00 AM - 12:00 PM",
                "max_participants": 20,
                "participants": ["isabella@mergington.edu", "james@mergington.edu"],
            },
            "Art Studio": {
                "description": "Explore painting, drawing, and mixed media",
                "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 15,
                "participants": ["grace@mergington.edu"],
            },
            "Music Band": {
                "description": "Play instruments and perform in concerts",
                "schedule": "Mondays, Wednesdays, Fridays, 3:30 PM - 4:30 PM",
                "max_participants": 25,
                "participants": ["lucas@mergington.edu", "mia@mergington.edu"],
            },
            "Science Club": {
                "description": "Conduct experiments and explore STEM topics",
                "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
                "max_participants": 18,
                "participants": ["ryan@mergington.edu"],
            },
            "Debate Team": {
                "description": "Develop argumentation and public speaking skills",
                "schedule": "Thursdays, 4:00 PM - 5:30 PM",
                "max_participants": 12,
                "participants": ["noah@mergington.edu", "ava@mergington.edu"],
            },
        }.items()
    }

    activities.clear()
    activities.update(original)

    yield


def test_root_redirects():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert "Chess Club" in response.json()


def test_signup_success():
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test@mergington.edu" in response.json()["message"]
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_activity_not_found():
    response = client.post("/activities/Unknown/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_signup_already_registered():
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400


def test_unregister_success():
    response = client.delete("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu" in response.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_activity_not_found():
    response = client.delete("/activities/Unknown/signup?email=test@mergington.edu")
    assert response.status_code == 404


def test_unregister_not_signed_up():
    response = client.delete("/activities/Chess%20Club/signup?email=unknown@mergington.edu")
    assert response.status_code == 400
