import copy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def restore_activities():
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))


_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


def test_unregister_participant_removes_email():
    restore_activities()

    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "Removed michael@mergington.edu" in response.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_unknown_participant_returns_404():
    restore_activities()

    response = client.delete("/activities/Chess Club/participants/ghost@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
