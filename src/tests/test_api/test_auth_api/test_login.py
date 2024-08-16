from src.main.security import get_password_hash
from src.adapters.sqlalchemy.models import User
from src.tests.conftest import client, test_db, db


def test_login(test_db, db):
    user = User(
        id=1,
        username="nazya08",
        email="nazya08@gmail.com",
        hashed_password=get_password_hash('1234'),
        type="admin",
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post("/api/auth/login", json={
        "email": "nazya08@gmail.com",
        "password": "1234"
    })

    tokens_response = response.json()

    assert response.status_code == 200
    assert "access_token" in tokens_response
    assert "refresh_token" in tokens_response
    assert "token_type" in tokens_response


def test_login_invalid_credentials(test_db, db):
    response = client.post("/api/auth/login", json={"email": "wrong@example.com", "password": "wrongpassword"})

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
