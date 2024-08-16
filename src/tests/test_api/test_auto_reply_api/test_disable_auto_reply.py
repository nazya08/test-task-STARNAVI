from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser


def test_disable_auto_reply(test_db, superuser):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    response = client.post(
        "/api/comments/disable-auto-reply/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Auto-reply disabled"
