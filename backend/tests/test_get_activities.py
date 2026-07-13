"""
Tests for GET /activities endpoint.
"""

import pytest
from backend.tests.utils import verify_activity_schema


class TestGetActivities:
    """Test suite for retrieving activities."""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities from the database."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Should return 8 activities
        assert len(data) == 8
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Tennis Club" in data
        assert "Art Studio" in data
        assert "Drama Club" in data
        assert "Robotics Club" in data
    
    def test_get_activities_returns_correct_structure(self, client, reset_activities):
        """Test that activities have the correct schema."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        activities_data = response.json()
        
        # Verify each activity has required fields
        for activity_name, activity_details in activities_data.items():
            assert isinstance(activity_name, str), f"Activity name should be string"
            verify_activity_schema(activity_details)
    
    def test_get_activities_contains_valid_participants(self, client, reset_activities):
        """Test that activities contain valid participant data."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        activities_data = response.json()
        
        # Check Chess Club has initial participants
        chess_club = activities_data["Chess Club"]
        assert len(chess_club["participants"]) >= 0
        assert isinstance(chess_club["participants"], list)
        
        # All participants should be email strings
        for participant in chess_club["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation
    
    def test_get_activities_contains_required_fields(self, client, reset_activities):
        """Test that activity details contain all required fields."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        activities_data = response.json()
        
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_details in activities_data.items():
            activity_fields = set(activity_details.keys())
            missing = required_fields - activity_fields
            
            assert not missing, f"Activity '{activity_name}' missing fields: {missing}"
