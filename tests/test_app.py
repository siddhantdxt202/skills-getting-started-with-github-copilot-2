from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Clean up in case the test is rerun within the same process.
    client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert delete_response.status_code == 200

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]
