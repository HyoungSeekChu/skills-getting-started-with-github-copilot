import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original_state))


client = TestClient(app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    post_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    assert post_response.status_code == 200

    delete_response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
