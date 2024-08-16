from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post, comment


def test_read_all_comments(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get(f"/api/posts/{post.id}/comments/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    # Якщо є коментарі, перевіримо, що вони належать до правильного поста
    if data:
        assert data[0]["post_id"] == post.id


def test_read_comment_by_id(test_db, superuser, post, comment):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get(f"/api/posts/{post.id}/comments/{comment.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == comment.id
    assert data["content"] == comment.content
    assert data["post_id"] == post.id

