from src.adapters.sqlalchemy.models import User
from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, default_user


def test_read_users_as_superuser(test_db, db, superuser):
    # Створення користувачів для перевірки
    user2 = User(username="user2", email="user2@example.com", hashed_password="hashedpassword", type="default_user")
    db.add(user2)
    db.commit()

    # Авторизація як суперюзер
    superuser_token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {superuser_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["users_list"]) == 2
    assert data["pagination_detail"]["total"] == 2


def test_read_user_by_id(test_db, superuser, default_user):
    superuser_token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.get("/api/users/2", headers={"Authorization": f"Bearer {superuser_token}"})

    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert "username" in data
    assert "email" in data

    assert data["id"] == 2
    assert data["username"] == "simple_user"
    assert data["email"] == "simple_user@example.com"
