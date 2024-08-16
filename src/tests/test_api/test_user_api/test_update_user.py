from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, default_user


def test_update_user(test_db, superuser):
    superuser_token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.put(
        "/api/users/1",
        headers={"Authorization": f"Bearer {superuser_token}"},
        json={
            "username": "updateduser",
            "email": "updateduser@example.com",
            "is_active": False
        })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "updateduser"
    assert data["email"] == "updateduser@example.com"
    assert data["is_active"] is False


def test_update_user_as_non_superuser(test_db, default_user):
    default_user_token = create_access_token(user_id=default_user.id, user_email=default_user.email)

    response = client.put(
        f"/api/users/{default_user.id}",
        headers={"Authorization": f"Bearer {default_user_token}"},
        json={
            "username": "updated_user",
            "email": "updated_user@example.com",
            "type": "default_user",
            "is_active": True
        })

    assert response.status_code == 400
    assert response.json()["detail"] == "The user doesn't have enough privileges"
