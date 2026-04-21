"""Tests for account signup and removal endpoints."""

import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_new_student_success(self, client):
        """Test successfully signing up a new student for an activity."""
        test_email = "newstudent@mergington.edu"
        response = client.post("/activities/Chess Club/signup", params={"email": test_email})

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_updates_participants_list(self, client):
        """Test that signup actually adds participant to activity."""
        test_email = "newstudent@mergington.edu"

        # Sign up
        client.post("/activities/Programming Class/signup", params={"email": test_email})

        # Verify participant was added
        response = client.get("/activities")
        activities = response.json()
        prog_class = activities["Programming Class"]
        assert test_email in prog_class["participants"]

    def test_signup_duplicate_email_returns_400(self, client):
        """Test that signing up the same email twice returns 400."""
        test_email = "michael@mergington.edu"  # Already in Chess Club

        response = client.post("/activities/Chess Club/signup", params={"email": test_email})
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        response = client.post("/activities/Fake Activity/signup", params={"email": "test@mergington.edu"})
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_signup_to_different_activity_same_email(self, client):
        """Test that same student can sign up for different activities."""
        # michael@mergington.edu is already in Chess Club
        # Try signing up to Programming Class
        response = client.post("/activities/Programming Class/signup", 
                              params={"email": "michael@mergington.edu"})

        assert response.status_code == 200
        data = response.json()
        assert "michael@mergington.edu" in data["message"]

    def test_signup_multiple_different_students(self, client):
        """Test that multiple different students can sign up."""
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

        for email in emails:
            response = client.post("/activities/Art Club/signup", params={"email": email})
            assert response.status_code == 200

        # Verify all were added
        response = client.get("/activities")
        activities = response.json()
        art_club = activities["Art Club"]

        for email in emails:
            assert email in art_club["participants"]

    def test_signup_with_empty_email(self, client):
        """Test signup with empty email parameter."""
        response = client.post("/activities/Chess Club/signup", params={"email": ""})
        # Empty string is still a string, so it will be added
        assert response.status_code == 200

    def test_signup_preserves_existing_participants(self, client):
        """Test that signup doesn't overwrite existing participants."""
        original_response = client.get("/activities")
        original_chess = original_response.json()["Chess Club"]["participants"].copy()

        new_email = "preservation@mergington.edu"
        client.post("/activities/Chess Club/signup", params={"email": new_email})

        updated_response = client.get("/activities")
        updated_chess = updated_response.json()["Chess Club"]["participants"]

        for original_participant in original_chess:
            assert original_participant in updated_chess


class TestRemoveSignup:
    """Test suite for DELETE /activities/{activity_name}/signup endpoint."""

    def test_remove_existing_participant_success(self, client):
        """Test successfully removing an existing participant."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.delete("/activities/Chess Club/signup", params={"email": email})

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Removed" in data["message"]

    def test_remove_updates_participants_list(self, client):
        """Test that remove actually removes participant from activity."""
        email = "michael@mergington.edu"

        # Remove
        client.delete("/activities/Chess Club/signup", params={"email": email})

        # Verify participant was removed
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        assert email not in chess_club["participants"]

    def test_remove_nonexistent_participant_returns_400(self, client):
        """Test that removing a participant not in activity returns 400."""
        response = client.delete("/activities/Chess Club/signup", 
                                params={"email": "notmember@mergington.edu"})
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client):
        """Test that removing from non-existent activity returns 404."""
        response = client.delete("/activities/Fake Activity/signup", 
                                params={"email": "test@mergington.edu"})
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_remove_then_readd_same_participant(self, client):
        """Test that a participant can be removed and added again."""
        email = "michael@mergington.edu"
        activity = "Chess Club"

        # Remove
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200

        # Try to add back
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200

        # Verify they're back in
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity]["participants"]

    def test_remove_one_participant_preserves_others(self, client):
        """Test that removing one participant doesn't affect others."""
        activity = "Music Ensemble"

        # Get original participants
        response = client.get("/activities")
        original_participants = response.json()[activity]["participants"].copy()

        # Remove first participant
        email_to_remove = original_participants[0]
        client.delete(f"/activities/{activity}/signup", params={"email": email_to_remove})

        # Check remaining participants
        response = client.get("/activities")
        updated_participants = response.json()[activity]["participants"]

        # Verify removed participant is gone
        assert email_to_remove not in updated_participants

        # Verify other participants are still there
        for participant in original_participants[1:]:
            assert participant in updated_participants

    def test_remove_all_participants_one_by_one(self, client):
        """Test removing all participants from an activity."""
        activity = "Swimming Club" if "Swimming Club" in client.get("/activities").json() else "Swimming Club"
        
        # Use an activity with fewer seeds to make test manageable
        # Let's just add 3 participants to Swim Club and remove them all
        emails = ["removeme1@mergington.edu", "removeme2@mergington.edu", "removeme3@mergington.edu"]

        # Add them
        for email in emails:
            client.post("/activities/Swim Club/signup", params={"email": email})

        # Remove them all
        for email in emails:
            response = client.delete("/activities/Swim Club/signup", params={"email": email})
            assert response.status_code == 200

        # Verify all are gone
        response = client.get("/activities")
        swim_club = response.json()["Swim Club"]
        for email in emails:
            assert email not in swim_club["participants"]


class TestSignupIntegration:
    """Integration tests for signup and remove workflow."""

    def test_signup_remove_signup_workflow(self, client):
        """Test a complete workflow of signup, remove, and signup again."""
        email = "workflow@mergington.edu"
        activity = "Debate Club"

        # Step 1: Sign up
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200

        # Step 2: Verify signup
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

        # Step 3: Remove
        response = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200

        # Step 4: Verify removal
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]

        # Step 5: Sign up again
        response = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response.status_code == 200

        # Step 6: Verify second signup
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

    def test_multiple_participants_concurrent_operations(self, client):
        """Test multiple participants being added and removed concurrently."""
        activity = "Science Club"
        
        # Add 5 participants
        new_participants = [f"student{i}@mergington.edu" for i in range(1, 6)]
        for email in new_participants:
            response = client.post(f"/activities/{activity}/signup", params={"email": email})
            assert response.status_code == 200

        # Remove every other participant
        for i, email in enumerate(new_participants):
            if i % 2 == 0:
                response = client.delete(f"/activities/{activity}/signup", params={"email": email})
                assert response.status_code == 200

        # Verify final state
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        
        for i, email in enumerate(new_participants):
            if i % 2 == 0:
                assert email not in participants
            else:
                assert email in participants
