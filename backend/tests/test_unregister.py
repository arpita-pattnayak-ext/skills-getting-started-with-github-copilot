"""
Tests for DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest
from backend.tests.utils import get_activity_by_name, add_participant_to_activity


class TestUnregister:
    """Test suite for activity unregister/removal functionality."""
    
    def test_unregister_participant_success(self, client, reset_activities):
        """Test successful removal of a participant from an activity."""
        activity_name = "Tennis Club"
        email = "isabella@mergington.edu"  # Existing participant in Tennis Club
        
        activity = get_activity_by_name(activity_name)
        assert email in activity["participants"]
        
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        
        assert response.status_code == 200
        assert response.json() == {"message": f"Removed {email} from {activity_name}"}
        
        # Verify participant was removed
        updated_activity = get_activity_by_name(activity_name)
        assert email not in updated_activity["participants"]
    
    def test_unregister_multiple_participants_sequentially(self, client, reset_activities):
        """Test removing multiple participants one by one."""
        activity_name = "Chess Club"
        initial_participants = get_activity_by_name(activity_name)["participants"].copy()
        
        for email in initial_participants:
            response = client.delete(f"/activities/{activity_name}/participants/{email}")
            assert response.status_code == 200
        
        # Verify all removed
        activity = get_activity_by_name(activity_name)
        assert len(activity["participants"]) == 0
    
    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities):
        """Test removing from non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/participants/test@mergington.edu"
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_nonexistent_participant_returns_404(self, client, reset_activities):
        """Test removing non-existent participant from activity returns 404."""
        response = client.delete(
            "/activities/Chess Club/participants/not-a-real@mergington.edu"
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
    
    def test_unregister_preserves_other_participants(self, client, reset_activities):
        """Test that unregistering one participant preserves others."""
        activity_name = "Programming Class"
        activity = get_activity_by_name(activity_name)
        original_participants = activity["participants"].copy()
        
        # Remove the first participant
        email_to_remove = original_participants[0]
        response = client.delete(f"/activities/{activity_name}/participants/{email_to_remove}")
        
        assert response.status_code == 200
        
        # Verify removed participant is gone
        updated_activity = get_activity_by_name(activity_name)
        assert email_to_remove not in updated_activity["participants"]
        
        # Verify other participants are still there
        for email in original_participants[1:]:
            assert email in updated_activity["participants"]
    
    def test_unregister_and_resign_up(self, client, reset_activities):
        """Test that participant can re-sign up after unregistering."""
        activity_name = "Robotics Club"
        email = "liam@mergington.edu"
        
        # Remove participant
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 200
        
        activity = get_activity_by_name(activity_name)
        assert email not in activity["participants"]
        
        # Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify re-signup succeeded
        activity = get_activity_by_name(activity_name)
        assert email in activity["participants"]
    
    def test_unregister_same_participant_twice_returns_404(self, client, reset_activities):
        """Test removing same participant twice returns 404 on second attempt."""
        activity_name = "Drama Club"
        email = "noah@mergington.edu"
        
        # First removal should succeed
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 200
        
        # Second removal should return 404
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Participant not found"
