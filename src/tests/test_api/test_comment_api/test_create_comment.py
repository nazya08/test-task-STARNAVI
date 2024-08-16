from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post


def test_create_comment(test_db, superuser, post):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    comment_data1 = {
        "content": "This is a new comment"
    }

    comment_data2 = {
        "content": "Damn and so stupid"
    }

    response1 = client.post(f"/api/posts/{post.id}/comments/", json=comment_data1,
                            headers={"Authorization": f"Bearer {token}"})

    response2 = client.post(f"/api/posts/{post.id}/comments/", json=comment_data2,
                            headers={"Authorization": f"Bearer {token}"})

    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["content"] == comment_data1["content"]
    assert data1["post_id"] == post.id
    assert data1["owner_id"] == superuser.id
    assert data1["is_blocked"] == False

    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["content"] == comment_data2["content"]
    assert data2["post_id"] == post.id
    assert data2["owner_id"] == superuser.id
    assert data2["is_blocked"] == True
