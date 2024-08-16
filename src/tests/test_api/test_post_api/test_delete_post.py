from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post


def test_delete_post(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.delete(f"/api/posts/{post.id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 204

    # Verify the post is deleted
    response = client.get(f"/api/posts/{post.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404
