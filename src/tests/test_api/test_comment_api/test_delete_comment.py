from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post, comment


def test_remove_comment(test_db, superuser, post, comment):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.delete(f"/api/posts/{post.id}/comments/{comment.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204  # No Content

    # Перевіряємо, що коментар дійсно видалений
    response = client.get(f"/api/posts/{post.id}/comments/{comment.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404  # Not Found
