"""
Utility functions and helpers for backend tests.
"""

import copy
from src.app import activities


# Store default state for reference
_DEFAULT_ACTIVITIES = copy.deepcopy(activities)


def reset_activities_to_default():
    """Reset activities to the default state."""
    activities.clear()
    activities.update(copy.deepcopy(_DEFAULT_ACTIVITIES))


def verify_activity_schema(activity: dict):
    """
    Verify that an activity response has the correct schema.
    
    Args:
        activity: Activity dict to validate
        
    Raises:
        AssertionError: If activity is missing required fields
    """
    required_fields = {"description", "schedule", "max_participants", "participants"}
    missing_fields = required_fields - set(activity.keys())
    
    if missing_fields:
        raise AssertionError(f"Activity missing required fields: {missing_fields}")
    
    # Verify field types
    assert isinstance(activity.get("description"), str), "description must be a string"
    assert isinstance(activity.get("schedule"), str), "schedule must be a string"
    assert isinstance(activity.get("max_participants"), int), "max_participants must be an integer"
    assert isinstance(activity.get("participants"), list), "participants must be a list"


def get_activity_by_name(activity_name: str):
    """Get an activity from the in-memory database by name."""
    return activities.get(activity_name)


def add_participant_to_activity(activity_name: str, email: str):
    """
    Directly add a participant to an activity (for setup).
    
    Args:
        activity_name: Name of the activity
        email: Email of the participant to add
    """
    if activity_name in activities:
        if email not in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].append(email)


def remove_participant_from_activity(activity_name: str, email: str):
    """
    Directly remove a participant from an activity (for cleanup).
    
    Args:
        activity_name: Name of the activity
        email: Email of the participant to remove
    """
    if activity_name in activities:
        if email in activities[activity_name]["participants"]:
            activities[activity_name]["participants"].remove(email)
