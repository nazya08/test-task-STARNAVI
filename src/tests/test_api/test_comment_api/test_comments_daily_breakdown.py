from datetime import datetime, timedelta

from src.main.security import create_access_token
from src.tests.conftest import client, test_db, db, superuser, post, comment


def test_comments_daily_breakdown(test_db, superuser, post, comment):
    token = create_access_token(user_id=superuser.id, user_email=superuser.email)

    today = datetime.today()
    start_date = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=2)).strftime('%Y-%m-%d')

    response = client.get(
        f"/api/posts/comments/daily_breakdown/?start_date={start_date}&end_date={end_date}&post_id={post.id}",
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()

    if data:
        first_entry = data[0]
        assert "total_comments" in first_entry
        assert first_entry["total_comments"] == 1
        assert first_entry["blocked_comments"] == 0
        assert first_entry["date"] == today.strftime('%Y-%m-%d')
