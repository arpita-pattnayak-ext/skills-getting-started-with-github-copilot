"""
Tests for POST /activities/{activity_name}/signup endpoint.
"""

import pytest
from backend.tests.utils import get_activity_by_name


class TestSignup:
    """Test suite for activity signup functionality."""
    
    def test_signup_for_activity_success(self, client, reset_activities, sample_email):
        """Test successful signup for an activity."""
        activity_name = "Chess Club"
        new_email = "newcomer@mergington.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {new_email} for {activity_name}"}
        
        # Verify participant was added to activity
        activity = get_activity_by_name(activity_name)
        assert new_email in activity["participants"]
    
    def test_signup_multiple_participants(self, client, reset_activities):
        """Test multiple different participants can sign up."""
        activity_name = "Programming Class"
        emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all participants were added
        activity = get_activity_by_name(activity_name)
        for email in emails:
            assert email in activity["participants"]
    
    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities, sample_email):
        """Test signup for non-existent activity returns 404."""
        response = client.post(
            f"/activities/Nonexistent Club/signup",
            params={"email": sample_email}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_already_registered_returns_400(self, client, reset_activities):
        """Test signup for already registered participant returns 400."""
        activity_name = "Tennis Club"
        email = "alex@mergington.edu"  # Already in Tennis Club
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    
    def test_signup_different_activities_same_email(self, client, reset_activities):
        """Test same student can sign up for multiple different activities."""
        email = "student@mergington.edu"
        activities_to_join = ["Chess Club", "Robotics Club", "Drama Club"]
        
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        for activity_name in activities_to_join:
            activity = get_activity_by_name(activity_name)
            assert email in activity["participants"]
    
    def test_signup_preserves_existing_participants(self, client, reset_activities):
        """Test that signup preserves existing participants list."""
        activity_name = "Art Studio"
        activity = get_activity_by_name(activity_name)
        original_participants = activity["participants"].copy()
        original_count = len(original_participants)
        
        new_email = "newstudent@mergington.edu"
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        assert response.status_code == 200
        
        # Check all original participants are still there
        updated_activity = get_activity_by_name(activity_name)
        for participant in original_participants:
            assert participant in updated_activity["participants"]
        
        # And count increased by 1
        assert len(updated_activity["participants"]) == original_count + 1
