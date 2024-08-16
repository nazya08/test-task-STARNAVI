from src.main.security import create_refresh_token
from src.adapters.sqlalchemy.models import User
from src.tests.conftest import client, test_db, db


def test_token_refresh(test_db, db):
    new_user = User(email="test@example.com", username="testuser", hashed_password="hashedpassword", is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    refresh_token = create_refresh_token(user_id=new_user.id, user_email=new_user.email)

    response = client.post("api/auth/token-refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert new_tokens["token_type"] == "bearer"


def test_token_refresh_invalid_token():
    response = client.post("api/auth/token-refresh", json={"refresh_token": "invalid_token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
