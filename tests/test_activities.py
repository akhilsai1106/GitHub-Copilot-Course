def test_get_activities(client):
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) == 9  # We have 9 activities

    # Check structure of activities
    for name, activity in activities.items():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)
        assert isinstance(activity["max_participants"], int)

def test_get_activities_structure(client):
    """Test specific activity structure"""
    response = client.get("/activities")
    activities = response.json()

    chess_club = activities["Chess Club"]
    assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
    assert chess_club["max_participants"] == 12
    assert len(chess_club["participants"]) >= 0  # At least empty list