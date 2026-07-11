import pytest
from taskflow.services.auth_service import create_user,authenticate_user
def test_create_user(app):
    with app.app_context():
        u=create_user("Jane Doe","JANE@EXAMPLE.COM","password123"); assert u.email=="jane@example.com" and u.check_password("password123")
def test_empty_name(app):
    with app.app_context(), pytest.raises(ValueError): create_user("","a@b.com","password123")
def test_invalid_email(app):
    with app.app_context(), pytest.raises(ValueError): create_user("A","bad","password123")
def test_weak_password(app):
    with app.app_context(), pytest.raises(ValueError): create_user("A","a@b.com","short")
def test_duplicate_email(app,user):
    with app.app_context(), pytest.raises(ValueError): create_user("Again","test@example.com","password123")
def test_auth_success(app,user):
    with app.app_context(): assert authenticate_user("TEST@example.com","password123").id==user.id
def test_auth_bad_password(app,user):
    with app.app_context(): assert authenticate_user("test@example.com","wrong") is None
def test_auth_nonexistent(app):
    with app.app_context(): assert authenticate_user("nobody@example.com","password123") is None
