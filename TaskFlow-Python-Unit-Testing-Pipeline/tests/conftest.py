import pytest
from taskflow import create_app
from config import TestingConfig
from taskflow.extensions import db
from taskflow.services.auth_service import create_user
from taskflow.services.task_service import create_task

@pytest.fixture
def app():
    app=create_app(TestingConfig)
    with app.app_context():
        db.drop_all(); db.create_all()
        yield app
        db.session.remove(); db.drop_all()

@pytest.fixture
def client(app): return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        u=create_user("Test User","test@example.com","password123"); _=u.id; return u

@pytest.fixture
def second_user(app):
    with app.app_context():
        u=create_user("Other User","other@example.com","password123"); _=u.id; return u

@pytest.fixture
def auth_client(client, user):
    client.post("/login",data={"email":"test@example.com","password":"password123"})
    return client

@pytest.fixture
def sample_task(app,user):
    with app.app_context():
        t=create_task(user.id,title="Study pytest",description="Write tests",category="Study",priority="High",status="Pending",due_date="2030-01-01"); _=t.id; return t
