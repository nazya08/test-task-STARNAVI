from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post


def test_read_all_posts(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get("/api/posts/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    print(data)

    assert isinstance(data, list)
    assert len(data) > 0
    assert len(data) == 1


def test_read_post_by_id(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get(f"/api/posts/{post.id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()

    assert data["post_detail"]["id"] == post.id
    assert data["post_detail"]["title"] == post.title
    assert data["post_detail"]["description"] == post.description
    assert data["post_detail"]["created_by_id"] == superuser.id


def test_read_user_posts(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get(f"/api/posts/user/{superuser.id}", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert len(data) == 1
    assert any(p["id"] == post.id for p in data)
