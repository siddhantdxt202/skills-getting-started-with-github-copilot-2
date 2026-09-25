from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_adds_email_to_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_signup_rejects_duplicate_email():
    # Arrange
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
