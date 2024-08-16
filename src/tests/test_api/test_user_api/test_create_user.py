from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, default_user


def test_create_user(test_db, superuser):
    superuser_token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.post(
        "/api/users/",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password12345"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"


def test_create_user_as_non_superuser(test_db, default_user):
    default_user_token = create_access_token(user_id=default_user.id, user_email=default_user.email)

    response = client.post(
        "/api/users/",
        headers={"Authorization": f"Bearer {default_user_token}"},
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password12345",
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The user doesn't have enough privileges"
