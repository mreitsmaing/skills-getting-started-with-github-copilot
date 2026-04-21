"""Pytest configuration and shared fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app
import src.app


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities database to initial state before each test."""
    # Store original activities
    original_activities = {
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
        "Soccer Team": {
            "description": "Team sports training, drills, and weekend matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 22,
            "participants": ["noah@mergington.edu", "lily@mergington.edu"]
        },
        "Swim Club": {
            "description": "Swimming practice and competitive swim meets",
            "schedule": "Mondays, Wednesdays, 5:00 PM - 6:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Practice instruments and perform school concerts",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["isabella@mergington.edu", "sophia@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking, research, and argument skills",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["liam@mergington.edu", "olivia@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "ella@mergington.edu"]
        }
    }
    
    # Reset the module-level activities dictionary
    src.app.activities.clear()
    src.app.activities.update(deepcopy(original_activities))
    
    yield
    
    # Clean up after test
    src.app.activities.clear()
    src.app.activities.update(deepcopy(original_activities))


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Provide the list of all activity names for tests."""
    return [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swim Club",
        "Art Club",
        "Music Ensemble",
        "Debate Club",
        "Science Club"
    ]
