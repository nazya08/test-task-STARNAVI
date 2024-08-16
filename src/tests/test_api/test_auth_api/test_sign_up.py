from src.adapters.sqlalchemy.models import User
from src.tests.conftest import client, test_db, db


def test_sign_up(test_db, db):
    response = client.post("api/auth/sign-up", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "Password12345"
    })

    assert response.status_code == 200
    sign_up_response = response.json()
    assert sign_up_response["user_detail"]["email"] == "newuser@example.com"
    assert "access_token" in sign_up_response["tokens"]
    assert "refresh_token" in sign_up_response["tokens"]


def test_sign_up_existing_user(test_db, db):
    new_user = User(
        email="existinguser@example.com",
        username="existinguser",
        hashed_password="hashedpassword",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response = client.post("api/auth/sign-up", json={
        "email": "existinguser@example.com",
        "username": "existinguser",
        "password": "password"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == 'User with this username already exists.'
