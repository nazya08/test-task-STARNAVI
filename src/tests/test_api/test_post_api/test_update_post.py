from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post


def test_update_post(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    updated_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }

    response = client.patch(f"/api/posts/{post.id}", json=updated_data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == updated_data["title"]
    assert data["description"] == updated_data["description"]
