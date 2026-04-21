"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_nine_activities(self, client):
        """Test that GET /activities returns all 9 activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9

    def test_activities_have_required_fields(self, client):
        """Test that each activity has all required fields."""
        response = client.get("/activities")
        activities = response.json()

        required_fields = {"description", "schedule", "max_participants", "participants"}

        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys()), \
                f"Activity '{activity_name}' missing required fields"

    def test_activities_have_correct_data_types(self, client):
        """Test that activity fields have correct data types."""
        response = client.get("/activities")
        activities = response.json()

        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["description"], str), \
                f"{activity_name}: description should be string"
            assert isinstance(activity_data["schedule"], str), \
                f"{activity_name}: schedule should be string"
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name}: max_participants should be integer"
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name}: participants should be list"
            for participant in activity_data["participants"]:
                assert isinstance(participant, str), \
                    f"{activity_name}: each participant should be string (email)"

    def test_chess_club_exists_and_has_participants(self, client):
        """Test that Chess Club is in the activities list."""
        response = client.get("/activities")
        activities = response.json()

        assert "Chess Club" in activities
        chess_club = activities["Chess Club"]
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
        assert chess_club["max_participants"] == 12
        assert len(chess_club["participants"]) > 0

    def test_programming_class_exists(self, client):
        """Test that Programming Class is in the activities list."""
        response = client.get("/activities")
        activities = response.json()

        assert "Programming Class" in activities
        prog_class = activities["Programming Class"]
        assert prog_class["max_participants"] == 20
        assert len(prog_class["participants"]) > 0

    def test_all_expected_activities_present(self, client, sample_activities):
        """Test that all expected activities are present."""
        response = client.get("/activities")
        activities = response.json()

        for activity_name in sample_activities:
            assert activity_name in activities, \
                f"Expected activity '{activity_name}' not found"

    def test_participants_are_email_format(self, client):
        """Test that all participants appear to have email addresses."""
        response = client.get("/activities")
        activities = response.json()

        for activity_name, activity_data in activities.items():
            for participant in activity_data["participants"]:
                assert "@" in participant and "." in participant, \
                    f"{activity_name}: '{participant}' doesn't look like an email"

    def test_max_participants_are_positive_integers(self, client):
        """Test that max_participants are positive integers."""
        response = client.get("/activities")
        activities = response.json()

        for activity_name, activity_data in activities.items():
            assert activity_data["max_participants"] > 0, \
                f"{activity_name}: max_participants should be positive"
