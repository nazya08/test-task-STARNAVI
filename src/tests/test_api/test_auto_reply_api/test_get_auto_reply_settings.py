from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser


def test_get_auto_reply_settings(test_db, superuser):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    # First check when settings are not enabled
    response = client.get(
        "/api/comments/auto-reply-settings/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_enabled"] is False
    assert data["reply_delay"] is None

    # Enable auto-reply and check settings
    client.post(
        "/api/comments/enable-auto-reply/?delay=5",
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.get(
        "/api/comments/auto-reply-settings/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_enabled"] is True
    assert data["reply_delay"] == 5
