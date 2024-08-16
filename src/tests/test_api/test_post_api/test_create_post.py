from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser


def test_create_post(test_db, superuser):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    post_data1 = {
        "title": "Damn asshole",
        "description": "New Post Description 1"
    }

    post_data2 = {
        "title": "New Post",
        "description": "New Post Description 2"
    }

    response1 = client.post("/api/posts/", json=post_data1, headers={"Authorization": f"Bearer {token}"})
    response2 = client.post("/api/posts/", json=post_data2, headers={"Authorization": f"Bearer {token}"})

    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["title"] == post_data1["title"]
    assert data1["description"] == post_data1["description"]
    assert data1["is_blocked"] == True

    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["title"] == post_data2["title"]
    assert data2["description"] == post_data2["description"]
    assert data2["is_blocked"] == False
