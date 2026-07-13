"""
Pytest configuration and shared fixtures for backend tests.
"""

import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities as app_activities


# Store the default activities state at import time
_DEFAULT_ACTIVITIES = copy.deepcopy(app_activities)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset activities to default state before and after each test.
    Prevents test pollution and ensures isolation.
    """
    from src.app import activities
    
    # Reset before test
    activities.clear()
    activities.update(copy.deepcopy(_DEFAULT_ACTIVITIES))
    
    yield activities
    
    # Reset after test
    activities.clear()
    activities.update(copy.deepcopy(_DEFAULT_ACTIVITIES))


@pytest.fixture
def sample_activity():
    """Provide sample activity data for testing."""
    return {
        "name": "Test Club",
        "description": "A test activity",
        "schedule": "Mondays, 3:00 PM - 4:00 PM",
        "max_participants": 10,
        "participants": []
    }


@pytest.fixture
def sample_email():
    """Provide a sample email for testing."""
    return "test@mergington.edu"
