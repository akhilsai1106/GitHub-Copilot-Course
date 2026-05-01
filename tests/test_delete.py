def test_delete_participant_success(client):
    """Test successful participant removal"""
    # First add a participant
    client.post("/activities/Gym%20Class/signup?email=remove@mergington.edu")

    # Then remove them
    response = client.delete("/activities/Gym%20Class/participants/remove@mergington.edu")
    assert response.status_code == 200

    result = response.json()
    assert "message" in result
    assert "remove@mergington.edu" in result["message"]

def test_delete_participant_not_found(client):
    """Test removing non-existent participant"""
    response = client.delete("/activities/Chess%20Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert result["detail"] == "Participant not found"

def test_delete_activity_not_found(client):
    """Test removing participant from non-existent activity"""
    response = client.delete("/activities/NonExistent/participants/test@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert result["detail"] == "Activity not found"