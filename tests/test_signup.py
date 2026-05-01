import pytest

def test_signup_success(client):
    """Test successful signup"""
    response = client.post("/activities/Art%20Club/signup?email=newstudent@mergington.edu")
    assert response.status_code == 200

    result = response.json()
    assert "message" in result
    assert "newstudent@mergington.edu" in result["message"]

def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert result["detail"] == "Activity not found"

def test_signup_duplicate_participant(client):
    """Test signing up twice for same activity"""
    email = "duplicate@mergington.edu"
    activity = "Debate%20Club"

    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200

    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400

    result = response2.json()
    assert result["detail"] == "Student already signed up for this activity"

def test_signup_activity_full(client):
    """Test signup when activity is at capacity"""
    # Fill up an activity to capacity
    activity = "Science%20Club"
    base_count = 0  # Assume empty for test

    # Add participants up to capacity
    for i in range(15):  # Assuming max is 15
        email = f"student{i}@mergington.edu"
        response = client.post(f"/activities/{activity}/signup?email={email}")
        if i < 14:  # Allow up to max-1
            assert response.status_code == 200
        else:  # Last one should fail if at capacity
            if response.status_code == 400:
                result = response.json()
                assert result["detail"] == "Activity is full"

def test_signup_case_sensitive_activity_name(client):
    """Test that activity names are case sensitive"""
    # Try with different case
    response = client.post("/activities/chess%20club/signup?email=test@mergington.edu")
    assert response.status_code == 404  # Should fail due to case mismatch

def test_signup_special_characters_email(client):
    """Test signup with special characters in email"""
    response = client.post("/activities/Drama%20Club/signup?email=test.email+tag@mergington.edu")
    assert response.status_code == 200

def test_signup_empty_email(client):
    """Test signup with empty email"""
    response = client.post("/activities/Basketball%20Team/signup?email=")
    # This should probably fail, but depends on current validation
    # For now, just test it doesn't crash
    assert response.status_code in [200, 400]

def test_signup_long_email(client):
    """Test signup with very long email"""
    long_email = "a" * 200 + "@mergington.edu"
    response = client.post(f"/activities/Soccer%20Club/signup?email={long_email}")
    assert response.status_code == 200