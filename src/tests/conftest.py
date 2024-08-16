import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.sqlalchemy.models import User, Post, Comment
from src.main.celery import celery_app
from src.main.main import app
from src.adapters.sqlalchemy.db.base_class import Base
from src.main.config import settings
from src.presentation.dependencies.base import get_db

engine = create_engine(settings.SQLALCHEMY_TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def superuser(db) -> User:
    superuser = User(
        username="superuser",
        email="superuser@example.com",
        hashed_password="hashedpassword",
        type="admin"
    )

    db.add(superuser)
    db.commit()
    db.refresh(superuser)
    return superuser


@pytest.fixture
def default_user(db) -> User:
    user = User(
        username="simple_user",
        email="simple_user@example.com",
        hashed_password="hashedpassword",
        type="default_user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def post(db, superuser: User):
    post = Post(title="Test Post", description="Test Description", created_by_id=superuser.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@pytest.fixture(scope="function")
def comment(db, superuser: User, post: Post):
    comment = Comment(content="Comment content 1", post_id=post.id, owner_id=superuser.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@pytest.fixture(scope='session', autouse=True)
def configure_test_celery():
    celery_app.conf.update(
        broker_url='memory://',
        result_backend='cache+memory://',
        task_always_eager=True,
        task_eager_propagates=True
    )
    yield


client = TestClient(app)
