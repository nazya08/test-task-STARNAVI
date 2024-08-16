from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post, comment, configure_test_celery


def test_schedule_auto_reply(test_db, superuser, post, comment):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    client.post(
        "/api/comments/enable-auto-reply/?delay=10",
        headers={"Authorization": f"Bearer {token}"}
    )

    response = client.post(
        f"/api/comments/schedule-auto-reply/?post_id={post.id}&comment_id={comment.id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Auto-reply scheduled"
