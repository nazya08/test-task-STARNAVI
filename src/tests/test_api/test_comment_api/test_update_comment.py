from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post, comment


def test_update_comment(test_db, superuser, post, comment):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    updated_data = {
        "content": "Updated comment content"
    }

    response = client.patch(
        f"/api/posts/{post.id}/comments/{comment.id}",
        json=updated_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == comment.id
    assert data["content"] == updated_data["content"]
